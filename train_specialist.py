"""WildSense Indian Flora Specialist Trainer.
Trains a lightweight, metric-aligned nearest-centroid botanical specialist
head using frozen FastViT ONNX embeddings extracted from vetted iNaturalist observations.

Preserves the global taxonomy table and production inference pipeline unchanged.
"""

import os
import sys
import json
import time
import numpy as np

WORKSPACE = os.path.dirname(os.path.abspath(__file__))
DATASET_ROOT = os.path.join(WORKSPACE, "data", "specialist_dataset")
CACHE_FILE = os.path.join(DATASET_ROOT, "cached_embeddings.npz")
MANIFEST_FILE = os.path.join(DATASET_ROOT, "embeddings_manifest.json")
ARTIFACT_OUTPUT = os.path.join(DATASET_ROOT, "indian_flora_specialist.npz")

TARGET_CLASSES = [
    {
        "scientific_name": "Ocimum tenuiflorum",
        "canonical_name": "Holy Basil",
        "regional_names": {"hi": "तुलसी", "bn": "তুলসী", "sa": "तुलसी"}
    },
    {
        "scientific_name": "Tagetes erecta",
        "canonical_name": "African Marigold",
        "regional_names": {"hi": "गेंदा", "bn": "গাঁদা"}
    },
    {
        "scientific_name": "Azadirachta indica",
        "canonical_name": "Neem Tree",
        "regional_names": {"hi": "नीम", "bn": "নিম", "sa": "निम्ब"}
    },
    {
        "scientific_name": "Nyctanthes arbor-tristis",
        "canonical_name": "Night-flowering Jasmine",
        "regional_names": {"hi": "हरसिंगार / पारिजात", "bn": "শিউলি", "sa": "पारिजात"}
    },
    {
        "scientific_name": "Butea monosperma",
        "canonical_name": "Flame of the Forest",
        "regional_names": {"hi": "पलाश", "bn": "পলাশ", "sa": "पलाश"}
    },
    {
        "scientific_name": "Moringa oleifera",
        "canonical_name": "Drumstick Tree",
        "regional_names": {"hi": "सहजन", "bn": "সজনে", "sa": "शोभाञ्जन"}
    },
    {
        "scientific_name": "Rosa chinensis",
        "canonical_name": "China Rose / Cultivated Rose",
        "regional_names": {"hi": "गुलाब", "bn": "গোলাপ"}
    }
]

def train_specialist():
    t0 = time.perf_counter()
    if not os.path.exists(CACHE_FILE) or not os.path.exists(MANIFEST_FILE):
        raise FileNotFoundError(f"Missing cache or manifest in {DATASET_ROOT}. Run extract_embeddings first.")

    npz = np.load(CACHE_FILE)
    embeddings = npz["embeddings"]
    keys = list(npz["keys"])
    key_to_idx = {k: i for i, k in enumerate(keys)}

    with open(MANIFEST_FILE, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    species_names = [t["scientific_name"] for t in TARGET_CLASSES]
    num_classes = len(species_names)
    centroids = np.zeros((num_classes, 1024), dtype=np.float32)
    sample_counts = {}

    # Fit prototypes strictly on train split
    for idx, sp in enumerate(TARGET_CLASSES):
        sci = sp["scientific_name"]
        train_keys = [
            m["key"] for m in manifest
            if m["split"] == "train" and m["taxon_name"] == sci
        ]
        sample_counts[sci] = len(train_keys)
        if not train_keys:
            raise ValueError(f"No training samples found for {sci}")
        
        train_vectors = np.array([embeddings[key_to_idx[k]] for k in train_keys])
        mean_v = np.mean(train_vectors, axis=0)
        norm = np.linalg.norm(mean_v)
        centroids[idx] = mean_v / max(norm, 1e-9)

    # Threshold calibration using validation split only
    val_sims_per_class = {sci: [] for sci in species_names}
    for m in manifest:
        if m["split"] == "val" and m["taxon_name"] in species_names:
            emb = embeddings[key_to_idx[m["key"]]]
            sims = emb @ centroids.T
            pred_idx = int(np.argmax(sims))
            pred_sci = species_names[pred_idx]
            if pred_sci == m["taxon_name"]:
                val_sims_per_class[pred_sci].append(float(sims[pred_idx]))

    class_thresholds = {}
    for sci, scores in val_sims_per_class.items():
        if scores:
            # Conservative threshold at minimum true positive validation similarity
            class_thresholds[sci] = round(float(np.min(scores)), 3)
        else:
            class_thresholds[sci] = 0.650

    elapsed = (time.perf_counter() - t0) * 1000

    # Save specialist artifact
    np.savez_compressed(
        ARTIFACT_OUTPUT,
        centroids=centroids,
        classes=np.array(species_names),
        metadata=json.dumps({
            "version": "1.0.0",
            "model_type": "NearestCentroidPrototype",
            "embedding_dim": 1024,
            "num_classes": num_classes,
            "classes_info": TARGET_CLASSES,
            "training_samples": sample_counts,
            "validation_thresholds": class_thresholds,
            "training_time_ms": round(elapsed, 2),
            "created_at": time.strftime("%Y-%m-%d %H:%M:%S")
        })
    )

    artifact_bytes = os.path.getsize(ARTIFACT_OUTPUT)
    print(f"Specialist trained successfully in {elapsed:.2f} ms")
    print(f"Artifact saved: {ARTIFACT_OUTPUT}")
    print(f"Artifact size: {artifact_bytes / 1024:.2f} KB ({artifact_bytes} bytes)")
    print(f"Classes: {num_classes}")
    for sp in TARGET_CLASSES:
        sci = sp["scientific_name"]
        print(f"  - {sci:25s}: N_train={sample_counts[sci]}, Val_threshold={class_thresholds.get(sci)}")

if __name__ == "__main__":
    train_specialist()
