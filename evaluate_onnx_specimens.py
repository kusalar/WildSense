import asyncio
import sys
from pathlib import Path

# Add backend directory to path
backend_dir = Path(__file__).resolve().parent / "backend"
sys.path.insert(0, str(backend_dir))

from services.onnx_botany_provider import ONNXBotanicalVisionProvider

async def evaluate_test_specimens():
    provider = ONNXBotanicalVisionProvider()
    assert await provider.is_available(), "Provider must be available"

    test_images = [
        ("neem", "test_specimens/neem.jpg", "Azadirachta indica (Neem)"),
        ("lotus", "test_specimens/lotus.jpg", "Nelumbo nucifera (Sacred Lotus)"),
        ("water_lily", "test_specimens/water_lily.jpg", "Nymphaea nouchali / alba (Water Lily)"),
        ("hibiscus", "test_specimens/hibiscus.jpg", "Hibiscus rosa-sinensis"),
        ("rose", "test_specimens/rose.jpg", "Rosa (Rose)"),
        ("marigold", "test_specimens/marigold.jpg", "Tagetes erecta (Marigold)"),
        ("tulsi", "test_specimens/tulsi.jpg", "Ocimum tenuiflorum (Holy Basil)"),
        ("non_plant_rock", "test_specimens/non_plant_rock.jpg", "Non-plant (Rock)"),
    ]

    print("=" * 80)
    print("STAGE 2 — ONNX BOTANICAL CLASSIFIER EVALUATION REPORT")
    print("=" * 80)

    for key, path_str, ground_truth in test_images:
        path = Path(path_str)
        if not path.exists():
            print(f"Skipping {key}: file not found")
            continue
        with open(path, "rb") as f:
            img_bytes = f.read()

        result = await provider.analyze_image(img_bytes)

        print(f"\n[Specimen: {key.upper()}]")
        print(f"  Ground Truth:    {ground_truth}")
        print(f"  Predicted Name:  {result.get('common_name')}")
        print(f"  Scientific Name: {result.get('scientific_name')}")
        print(f"  Confidence:      {result.get('confidence')} (raw cosine: {result.get('raw_cosine')})")
        print(f"  Category:        {result.get('category')}")
        print(f"  Inference Time:  {result.get('inference_ms')} ms")
        print(f"  Uncertainty:     {result.get('uncertainty')[:120]}...")
        print("  Top-3 Candidates:")
        for cand in result.get("candidates", [])[:3]:
            print(f"    #{cand['rank']}: {cand['scientific_name']} (cosine: {cand['cosine_score']})")

if __name__ == "__main__":
    asyncio.run(evaluate_test_specimens())
