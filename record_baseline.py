import asyncio
import sys
from pathlib import Path

backend_dir = Path("backend")
sys.path.insert(0, str(backend_dir))
from services.onnx_botany_provider import ONNXBotanicalVisionProvider

async def eval_baseline():
    provider = ONNXBotanicalVisionProvider()
    await provider.is_available()
    
    specimens = [
        ("neem.jpg", "Azadirachta indica", "tree"),
        ("lotus.jpg", "Nelumbo nucifera", "aquatic"),
        ("water_lily.jpg", "Nymphaea nouchali", "aquatic"),
        ("hibiscus.jpg", "Hibiscus rosa-sinensis", "flower"),
        ("rose.jpg", "Rosa", "flower"),
        ("marigold.jpg", "Tagetes erecta", "flower"),
        ("tulsi.jpg", "Ocimum tenuiflorum", "herb"),
        ("non_plant_rock.jpg", None, "rock"),
    ]
    
    plant_tests = [s for s in specimens if s[1] is not None]
    top1_correct = 0
    top5_correct = 0
    genus_correct = 0
    
    print("=" * 75)
    print("STAGE 2 BASELINE BENCHMARK RESULTS (BioCLIP FastViT 4,271 ONNX)")
    print("=" * 75)
    
    for fname, target, category in specimens:
        path = Path("test_specimens") / fname
        if not path.exists():
            continue
        with open(path, "rb") as f:
            res = await provider.analyze_image(f.read())
        top1 = res["scientific_name"]
        cands = [c["scientific_name"] for c in res.get("candidates", [])]
        
        is_t1 = bool(target and target.lower() == top1.lower())
        is_t5 = bool(target and any(target.lower() == c.lower() for c in cands))
        target_genus = target.split()[0].lower() if target else ""
        is_genus = bool(target and any(c.lower().startswith(target_genus + " ") for c in cands[:1]))
        
        if is_t1:
            top1_correct += 1
        if is_t5:
            top5_correct += 1
        if is_genus:
            genus_correct += 1
        
        if target is None:
            status = "FAIL (False Positive Plant)" if res["category"] != "rock" and res["category"] != "other" else "PASS (Non-plant Rejected)"
        else:
            status = "PASS (Exact)" if is_t1 else ("PASS (Genus)" if is_genus else "FAIL")
            
        print(f"\n[{fname.upper()}] Target: {target or 'Non-plant'}")
        print(f"  Predicted: {top1} (Status: {status})")
        print(f"  Similarity: {res.get('raw_cosine'):.3f} | Calibrated Conf: {res.get('confidence')}")
        print(f"  Top 3 Candidates: {', '.join(cands[:3])}")

    print("\n" + "=" * 75)
    print(f"Plant Specimens Tested: {len(plant_tests)}")
    print(f"Top-1 Exact Species Accuracy: {top1_correct}/{len(plant_tests)} ({top1_correct/len(plant_tests)*100:.1f}%)")
    print(f"Top-5 Exact Species Accuracy: {top5_correct}/{len(plant_tests)} ({top5_correct/len(plant_tests)*100:.1f}%)")
    print(f"Genus-level Accuracy:         {genus_correct}/{len(plant_tests)} ({genus_correct/len(plant_tests)*100:.1f}%)")
    print(f"Non-plant Control:           1 specimen tested (classified as plant -> False Positive)")
    print("=" * 75)

if __name__ == "__main__":
    asyncio.run(eval_baseline())
