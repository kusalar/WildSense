"""WildSense Stage 5: Safe Global + Indian Flora Specialist Arbitration Benchmark.

Reproducible evaluation script comparing:
1. Global 4,271-class FastViT baseline.
2. 7-class Indian Flora Specialist head (unconstrained).
3. Safe Multi-Gate Arbitration pipeline.

Evaluates:
- Baseline specimens (test_specimens/): lotus, hibiscus, water_lily, neem, tulsi, marigold, rose, non_plant_rock.
- Held-out unseen observations (N=28, 4 per species).
- Sweet Basil controls (Ocimum basilicum, N=8).
- Validation observations (N=28).
"""

import os
import sys
import json
import numpy as np

WORKSPACE = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.join(WORKSPACE, "backend")
DATASET_ROOT = os.path.join(WORKSPACE, "data", "specialist_dataset")
CACHE_FILE = os.path.join(DATASET_ROOT, "cached_embeddings.npz")
MANIFEST_FILE = os.path.join(DATASET_ROOT, "embeddings_manifest.json")
ARTIFACT_FILE = os.path.join(DATASET_ROOT, "indian_flora_specialist.npz")
TAXA_TABLE_PATH = os.path.join(BACKEND_DIR, "models_onnx", "taxa_table.npy")
TAXA_LABELS_PATH = os.path.join(BACKEND_DIR, "models_onnx", "taxa_labels.json")

sys.path.insert(0, BACKEND_DIR)
from services.specialist_arbitrator import SpecialistArbitrator, DEV_THRESHOLDS

def run_benchmark():
    global_table = np.load(TAXA_TABLE_PATH)
    with open(TAXA_LABELS_PATH, "r", encoding="utf-8") as f:
        global_labels = json.load(f)

    npz = np.load(CACHE_FILE)
    embeddings = npz["embeddings"]
    keys = list(npz["keys"])
    key_to_idx = {k: i for i, k in enumerate(keys)}

    with open(MANIFEST_FILE, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    arbitrator = SpecialistArbitrator(artifact_path=ARTIFACT_FILE)
    arbitrator.load()
    classes = arbitrator._classes

    print("=" * 85)
    print("STAGE 5: SAFE GLOBAL + INDIAN FLORA SPECIALIST ARBITRATION BENCHMARK")
    print("=" * 85)
    print(f"Specialist Head: {len(classes)} regional species")
    print(f"Global Model:    4,271 open-vocabulary plant taxa")
    print(f"Thresholds (Dev): {DEV_THRESHOLDS}")
    print("-" * 85)

    def evaluate_item(emb, optical_ok=True, optical_warns=None):
        # 1. Global top-1
        g_sims = emb @ global_table.T
        top_g_idx = int(np.argmax(g_sims))
        top_g_sci = global_labels[top_g_idx]["scientific"]
        top_g_score = float(g_sims[top_g_idx])
        top_g_cands = [{"scientific_name": top_g_sci, "similarity_score": round(top_g_score, 3), "match_level": "exact"}]

        # 2. Specialist top-1 (unconstrained)
        spec_cands = arbitrator.score_specialist(emb)
        top_s_sci = spec_cands[0]["scientific_name"]
        top_s_score = spec_cands[0]["similarity_score"]

        # 3. Arbitrated result
        arb_diag = arbitrator.arbitrate(
            emb,
            top_g_cands,
            {"acceptable": optical_ok, "warnings": optical_warns or []}
        )
        return {
            "global_sci": top_g_sci,
            "global_score": top_g_score,
            "spec_sci": top_s_sci,
            "spec_score": top_s_score,
            "arb": arb_diag
        }

    # --- 1. Baseline Specimens ---
    print("\n[1] BASELINE TEST SPECIMENS (test_specimens/)")
    print(f"{'Specimen':16s} | {'Global Top-1':22s} | {'Specialist Only':22s} | {'Arbitrated Result':24s} | Source")
    print("-" * 105)
    baseline_specs = ['neem', 'tulsi', 'marigold', 'rose', 'lotus', 'hibiscus', 'water_lily', 'non_plant_rock']
    for b in baseline_specs:
        k = f"baseline_{b}.jpg"
        if k not in key_to_idx:
            continue
        emb = embeddings[key_to_idx[k]]
        opt_ok = True
        opt_warn = []
        if b == "non_plant_rock":
            opt_ok = False
            opt_warn.append("Zero vegetation variance; stone texture.")

        res = evaluate_item(emb, opt_ok, opt_warn)
        arb = res["arb"]
        chosen = arb.get("specialist_candidate") if arb.get("use_specialist") else arb.get("global_candidate", res["global_sci"])
        src = arb.get("chosen_source", "global")
        if arb.get("decision") == "optical_rejection":
            chosen = "Optical Rejection"
            src = "safeguard"
        print(f"{b:16s} | {res['global_sci'][:20]:20s} ({res['global_score']:.2f}) | {res['spec_sci'][:20]:20s} ({res['spec_score']:.2f}) | {chosen[:22]:22s} | {src}")

    # --- 2. Held-out Test Set (N=28) ---
    test_items = [m for m in manifest if m["split"] == "test" and m["taxon_name"] in classes]
    print(f"\n[2] HELD-OUT TEST OBSERVATIONS (N={len(test_items)})")
    
    glob_exact = 0
    glob_genus = 0
    spec_exact = 0
    arb_exact = 0
    arb_accepted = 0
    arb_abstained = 0

    for it in test_items:
        true_sp = it["taxon_name"]
        emb = embeddings[key_to_idx[it["key"]]]
        res = evaluate_item(emb)
        arb = res["arb"]

        # Global metrics
        if res["global_sci"].lower() == true_sp.lower():
            glob_exact += 1
        if res["global_sci"].split()[0].lower() == true_sp.split()[0].lower():
            glob_genus += 1

        # Unconstrained specialist metrics
        if res["spec_sci"] == true_sp:
            spec_exact += 1

        # Arbitrated metrics
        if arb.get("use_specialist"):
            arb_accepted += 1
            if arb.get("specialist_candidate") == true_sp:
                arb_exact += 1
        else:
            arb_abstained += 1
            if res["global_sci"].lower() == true_sp.lower():
                arb_exact += 1

    total_test = len(test_items)
    print(f"Global 4,271 Baseline Model:")
    print(f"  - Exact Species Accuracy: {glob_exact}/{total_test} ({glob_exact/total_test*100:.1f}%)")
    print(f"  - Genus Match Accuracy:   {glob_genus}/{total_test} ({glob_genus/total_test*100:.1f}%)")
    print(f"Specialist Head (Unconstrained):")
    print(f"  - Top-1 Exact Accuracy:   {spec_exact}/{total_test} ({spec_exact/total_test*100:.1f}%)")
    print(f"Safe Arbitrated Pipeline:")
    print(f"  - Coverage (Specialist Accepted): {arb_accepted}/{total_test} ({arb_accepted/total_test*100:.1f}%)")
    print(f"  - Abstention Rate (Fell back to Global): {arb_abstained}/{total_test} ({arb_abstained/total_test*100:.1f}%)")
    acc_among_accepted = (arb_exact / arb_accepted * 100) if arb_accepted > 0 else 0
    print(f"  - Accuracy among Accepted Predictions: {arb_exact}/{arb_accepted} ({acc_among_accepted:.1f}%)")

    # --- 3. Ocimum basilicum Controls (N=8) ---
    control_items = [m for m in manifest if m["split"] == "control"]
    print(f"\n[3] SWEET BASIL CONTROLS (Ocimum basilicum, N={len(control_items)})")
    for it in control_items:
        emb = embeddings[key_to_idx[it["key"]]]
        res = evaluate_item(emb)
        arb = res["arb"]
        chosen = arb.get("specialist_candidate") if arb.get("use_specialist") else res["global_sci"]
        conf_lvl = arb.get("match_level", "uncertain")
        src = arb.get("chosen_source", "global")
        print(f"  Obs {it['observation_id']}: Chosen={chosen:22s} | Conf={conf_lvl:15s} | Src={src:10s} | Score={res['spec_score']:.3f}")
        for w in arb.get("warnings", []):
            if "Sweet Basil" in w:
                print(f"    -> Explicit Caveat: {w}")

    print("=" * 85)

    # Save machine-readable results
    output_json_path = os.path.join(DATASET_ROOT, "stage6_benchmark_results.json")
    results_payload = {
        "benchmark_name": "WildSense Stage 6 Final Arbitration Benchmark",
        "timestamp": os.getenv("BENCHMARK_TIMESTAMP", "2026-10-10"),
        "dev_thresholds": DEV_THRESHOLDS,
        "summary": {
            "held_out_count": total_test,
            "global_exact_count": glob_exact,
            "global_exact_accuracy": round(glob_exact / total_test, 4),
            "global_genus_count": glob_genus,
            "global_genus_accuracy": round(glob_genus / total_test, 4),
            "specialist_unconstrained_count": spec_exact,
            "specialist_unconstrained_accuracy": round(spec_exact / total_test, 4),
            "arbitrated_accepted_count": arb_accepted,
            "arbitrated_coverage": round(arb_accepted / total_test, 4),
            "arbitrated_abstained_count": arb_abstained,
            "arbitrated_abstention_rate": round(arb_abstained / total_test, 4),
            "arbitrated_exact_count": arb_exact,
            "accuracy_among_accepted": round(arb_exact / arb_accepted, 4) if arb_accepted > 0 else 0.0
        },
        "baseline_specimens": [
            {
                "specimen": b,
                "global_top1": evaluate_item(embeddings[key_to_idx[f"baseline_{b}.jpg"]], b != "non_plant_rock", ["Zero vegetation variance; stone texture."] if b == "non_plant_rock" else [])["global_sci"],
                "global_score": round(evaluate_item(embeddings[key_to_idx[f"baseline_{b}.jpg"]], b != "non_plant_rock", ["Zero vegetation variance; stone texture."] if b == "non_plant_rock" else [])["global_score"], 3),
                "specialist_top1": evaluate_item(embeddings[key_to_idx[f"baseline_{b}.jpg"]], b != "non_plant_rock", ["Zero vegetation variance; stone texture."] if b == "non_plant_rock" else [])["spec_sci"],
                "specialist_score": round(evaluate_item(embeddings[key_to_idx[f"baseline_{b}.jpg"]], b != "non_plant_rock", ["Zero vegetation variance; stone texture."] if b == "non_plant_rock" else [])["spec_score"], 3),
                "arbitrated_result": evaluate_item(embeddings[key_to_idx[f"baseline_{b}.jpg"]], b != "non_plant_rock", ["Zero vegetation variance; stone texture."] if b == "non_plant_rock" else [])["arb"].get("specialist_candidate") if evaluate_item(embeddings[key_to_idx[f"baseline_{b}.jpg"]], b != "non_plant_rock", ["Zero vegetation variance; stone texture."] if b == "non_plant_rock" else [])["arb"].get("use_specialist") else ("Optical Rejection" if evaluate_item(embeddings[key_to_idx[f"baseline_{b}.jpg"]], b != "non_plant_rock", ["Zero vegetation variance; stone texture."] if b == "non_plant_rock" else [])["arb"].get("decision") == "optical_rejection" else evaluate_item(embeddings[key_to_idx[f"baseline_{b}.jpg"]], b != "non_plant_rock", ["Zero vegetation variance; stone texture."] if b == "non_plant_rock" else [])["global_sci"]),
                "chosen_source": evaluate_item(embeddings[key_to_idx[f"baseline_{b}.jpg"]], b != "non_plant_rock", ["Zero vegetation variance; stone texture."] if b == "non_plant_rock" else [])["arb"].get("chosen_source", "global"),
                "warnings": evaluate_item(embeddings[key_to_idx[f"baseline_{b}.jpg"]], b != "non_plant_rock", ["Zero vegetation variance; stone texture."] if b == "non_plant_rock" else [])["arb"].get("warnings", [])
            }
            for b in baseline_specs if f"baseline_{b}.jpg" in key_to_idx
        ],
        "held_out_predictions": [
            {
                "observation_id": it["observation_id"],
                "true_species": it["taxon_name"],
                "global_top1": evaluate_item(embeddings[key_to_idx[it["key"]]])["global_sci"],
                "global_score": round(evaluate_item(embeddings[key_to_idx[it["key"]]])["global_score"], 3),
                "specialist_top1": evaluate_item(embeddings[key_to_idx[it["key"]]])["spec_sci"],
                "specialist_score": round(evaluate_item(embeddings[key_to_idx[it["key"]]])["spec_score"], 3),
                "arbitrated_result": evaluate_item(embeddings[key_to_idx[it["key"]]])["arb"].get("specialist_candidate") if evaluate_item(embeddings[key_to_idx[it["key"]]])["arb"].get("use_specialist") else evaluate_item(embeddings[key_to_idx[it["key"]]])["global_sci"],
                "chosen_source": evaluate_item(embeddings[key_to_idx[it["key"]]])["arb"].get("chosen_source", "global"),
                "specialist_accepted": evaluate_item(embeddings[key_to_idx[it["key"]]])["arb"].get("use_specialist", False),
                "correct": (evaluate_item(embeddings[key_to_idx[it["key"]]])["arb"].get("specialist_candidate") == it["taxon_name"]) if evaluate_item(embeddings[key_to_idx[it["key"]]])["arb"].get("use_specialist") else (evaluate_item(embeddings[key_to_idx[it["key"]]])["global_sci"].lower() == it["taxon_name"].lower()),
                "warnings": evaluate_item(embeddings[key_to_idx[it["key"]]])["arb"].get("warnings", [])
            }
            for it in test_items
        ],
        "control_predictions": [
            {
                "observation_id": it["observation_id"],
                "true_species": it["taxon_name"],
                "specialist_top1": evaluate_item(embeddings[key_to_idx[it["key"]]])["spec_sci"],
                "specialist_score": round(evaluate_item(embeddings[key_to_idx[it["key"]]])["spec_score"], 3),
                "arbitrated_result": evaluate_item(embeddings[key_to_idx[it["key"]]])["arb"].get("specialist_candidate") if evaluate_item(embeddings[key_to_idx[it["key"]]])["arb"].get("use_specialist") else evaluate_item(embeddings[key_to_idx[it["key"]]])["global_sci"],
                "chosen_source": evaluate_item(embeddings[key_to_idx[it["key"]]])["arb"].get("chosen_source", "global"),
                "match_level": evaluate_item(embeddings[key_to_idx[it["key"]]])["arb"].get("match_level", "uncertain"),
                "warnings": evaluate_item(embeddings[key_to_idx[it["key"]]])["arb"].get("warnings", [])
            }
            for it in control_items
        ]
    }
    with open(output_json_path, "w", encoding="utf-8") as f_out:
        json.dump(results_payload, f_out, indent=2)
    print(f"\nMachine-readable benchmark results saved to: {output_json_path}")

if __name__ == "__main__":
    run_benchmark()
