"""WildSense Indian Flora Specialist Evaluator.
Executes rigorous evaluation comparing:
1. Nearest-Centroid Specialist vs. Baseline FastViT ONNX (4,271 classes).
2. Performance on held-out unseen test observations (28 specimens).
3. Near-neighbor control species (Ocimum basilicum) false positive sensitivity.
4. Existing baseline specimen evaluation (test_specimens/).
"""

import os
import sys
import json
import numpy as np

WORKSPACE = os.path.dirname(os.path.abspath(__file__))
DATASET_ROOT = os.path.join(WORKSPACE, "data", "specialist_dataset")
CACHE_FILE = os.path.join(DATASET_ROOT, "cached_embeddings.npz")
MANIFEST_FILE = os.path.join(DATASET_ROOT, "embeddings_manifest.json")
ARTIFACT_FILE = os.path.join(DATASET_ROOT, "indian_flora_specialist.npz")
TAXA_TABLE_PATH = os.path.join(WORKSPACE, "backend", "models_onnx", "taxa_table.npy")
TAXA_LABELS_PATH = os.path.join(WORKSPACE, "backend", "models_onnx", "taxa_labels.json")

def evaluate():
    # Load assets
    global_table = np.load(TAXA_TABLE_PATH)
    with open(TAXA_LABELS_PATH, "r", encoding="utf-8") as f:
        global_labels = json.load(f)

    npz_data = np.load(CACHE_FILE)
    embeddings = npz_data["embeddings"]
    keys = list(npz_data["keys"])
    key_to_idx = {k: i for i, k in enumerate(keys)}

    with open(MANIFEST_FILE, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    spec_data = np.load(ARTIFACT_FILE)
    centroids = spec_data["centroids"]
    classes = list(spec_data["classes"])
    meta = json.loads(str(spec_data["metadata"]))
    thresholds = meta["validation_thresholds"]

    test_items = [m for m in manifest if m["split"] == "test" and m["taxon_name"] in classes]
    
    print("=" * 80)
    print("WILD SENSE STAGE 4: INDIAN FLORA SPECIALIST BENCHMARK REPORT")
    print("=" * 80)
    print(f"Artifact: {ARTIFACT_FILE} ({os.path.getsize(ARTIFACT_FILE)/1024:.2f} KB)")
    print(f"Embedding Space: 1024-d L2-normalized FastViT Student")
    print(f"Target Species: {len(classes)}")
    print(f"Held-out Unseen Test Observations: {len(test_items)}")
    print("-" * 80)

    # 1. Held-out test evaluation
    per_class_results = {c: {"total": 0, "correct_top1": 0, "sims": []} for c in classes}
    global_top1_correct = 0
    global_genus_correct = 0
    specialist_top1_correct = 0

    print(f"\n[1] HELD-OUT TEST SPECIMENS (N={len(test_items)})")
    print(f"{'Species':24s} | {'Obs ID':10s} | {'Global Top-1':22s} | {'Specialist Top-1':22s} (Sim) | Match")
    print("-" * 85)

    for item in test_items:
        true_sp = item["taxon_name"]
        emb = embeddings[key_to_idx[item["key"]]]
        
        # Global model
        g_sims = emb @ global_table.T
        top_g_idx = int(np.argmax(g_sims))
        top_g_sci = global_labels[top_g_idx]["scientific"]
        top_g_score = float(g_sims[top_g_idx])
        
        # Specialist
        s_sims = emb @ centroids.T
        top_s_idx = int(np.argmax(s_sims))
        top_s_sci = classes[top_s_idx]
        top_s_score = float(s_sims[top_s_idx])
        
        is_spec_correct = (top_s_sci == true_sp)
        if is_spec_correct:
            specialist_top1_correct += 1
            per_class_results[true_sp]["correct_top1"] += 1
            
        per_class_results[true_sp]["total"] += 1
        per_class_results[true_sp]["sims"].append(top_s_score)
        
        if top_g_sci.lower() == true_sp.lower():
            global_top1_correct += 1
        if top_g_sci.split()[0].lower() == true_sp.split()[0].lower():
            global_genus_correct += 1
            
        mark = "[OK]" if is_spec_correct else "[X] "
        print(f"{true_sp:24s} | {str(item['observation_id']):10s} | {top_g_sci[:22]:22s} | {top_s_sci[:22]:22s} ({top_s_score:.3f}) | {mark}")

    print("-" * 85)
    print(f"Overall Held-out Accuracy:")
    print(f"  - Baseline Global Model Exact Species: {global_top1_correct}/{len(test_items)} ({global_top1_correct/len(test_items)*100:.1f}%)")
    print(f"  - Baseline Global Model Genus Match:   {global_genus_correct}/{len(test_items)} ({global_genus_correct/len(test_items)*100:.1f}%)")
    print(f"  - Specialist Prototype Top-1 Accuracy: {specialist_top1_correct}/{len(test_items)} ({specialist_top1_correct/len(test_items)*100:.1f}%)")

    # Per-class summary
    print("\nPer-Class Breakdown:")
    for c in classes:
        st = per_class_results[c]
        acc = (st["correct_top1"] / st["total"] * 100) if st["total"] > 0 else 0
        avg_sim = np.mean(st["sims"]) if st["sims"] else 0
        print(f"  - {c:25s}: Top-1={st['correct_top1']}/{st['total']} ({acc:5.1f}%) | Mean Sim={avg_sim:.3f} | Threshold={thresholds.get(c)}")

    # 2. Control species
    control_items = [m for m in manifest if m["split"] == "control"]
    print(f"\n[2] CONTROL / CONFUSER EVALUATION (Ocimum basilicum, N={len(control_items)})")
    tulsi_idx = classes.index("Ocimum tenuiflorum")
    for it in control_items:
        emb = embeddings[key_to_idx[it["key"]]]
        s_sims = emb @ centroids.T
        top_idx = int(np.argmax(s_sims))
        tulsi_sim = float(s_sims[tulsi_idx])
        print(f"  Obs {it['observation_id']}: Top Pred={classes[top_idx]:24s} ({s_sims[top_idx]:.3f}) | Tulsi Sim={tulsi_sim:.3f}")

    # 3. Baseline specimens
    print("\n[3] EXISTING BASELINE SPECIMENS (test_specimens/)")
    baseline_specs = ['neem', 'tulsi', 'marigold', 'rose', 'lotus', 'hibiscus', 'water_lily', 'non_plant_rock']
    for b in baseline_specs:
        k = f"baseline_{b}.jpg"
        if k in key_to_idx:
            emb = embeddings[key_to_idx[k]]
            s_sims = emb @ centroids.T
            top_idx = int(np.argmax(s_sims))
            g_sims = emb @ global_table.T
            top_g_idx = int(np.argmax(g_sims))
            print(f"  Specimen {b:15s} -> Global: {global_labels[top_g_idx]['scientific'][:20]:20s} ({g_sims[top_g_idx]:.3f}) | Specialist: {classes[top_idx]:22s} ({s_sims[top_idx]:.3f})")

    print("=" * 80)

if __name__ == "__main__":
    evaluate()
