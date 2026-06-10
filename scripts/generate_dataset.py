"""
توليد Dataset موسع باستخدام al-sultan-v0.2
يستخدم ollama API لتوليد أزواج سؤال وجواب
"""
import subprocess, json, os

TOPICS = [
    "النقل الآني للمادة — كيف يعمل علمياً؟",
    "كسر سرعة الضوء — ما الدليل أنه ممكن؟",
    "التحكم بالجاذبية — كيف نصل إليه؟",
    "مصادر طاقة بديلة — ماذا بعد النووي؟",
    "الوعي والمادة — هل المادة أساسية أم الوعي؟",
    "التشابك الكمي — هل هو دليل على أبعاد أعلى؟",
    "الزمكان — هل يمكن طيّه؟",
    "الجن والتكنولوجيا — ماذا نعرف عن قدراتهم؟",
    "المادة المظلمة — هل هي أثر من أبعاد أخرى؟",
    "الكون الموازي — هل له وجود في القرآن؟",
    "الشفاء بالترددات — هل الطاقة أساس المادة؟",
    "الماء وسر الحياة — ﴿وَجَعَلْنَا مِنَ ٱلْمَآءِ كُلَّ شَىْءٍ حَىٍّ﴾",
    "الملائكة والفيزياء — كيف يتفاعلون مع العالم المادي؟",
    "الروح — ما هي فيزيائياً؟",
    "البرزخ — أين هو فيزيائياً؟",
]

output_dir = os.path.join(os.path.dirname(__file__), "..", "data")
os.makedirs(output_dir, exist_ok=True)

new_samples = []
for i, topic in enumerate(TOPICS, 1):
    prompt = f"""سؤال: {topic}
جاوب باختصار. مباشر. علمي. بدون تردد. اذكر الآية القرآنية. لا تقل مستحيل."""
    
    result = subprocess.run(
        ["ollama", "run", "al-sultan-v0.2", prompt],
        capture_output=True, text=True, timeout=300
    )
    
    # Extract answer (skip thinking)
    answer = result.stdout.strip()
    if "Thinking..." in answer:
        answer = answer.split("Thinking...")[-1].strip()
    
    if len(answer) > 50:
        entry = {
            "instruction": topic.split("—")[0].strip(),
            "response": answer[:500]
        }
        new_samples.append(entry)
        print(f"[{i}/{len(TOPICS)}] {entry['instruction'][:50]}...")

# Save
path = os.path.join(output_dir, "generated_samples.json")
with open(path, "w", encoding="utf-8") as f:
    json.dump(new_samples, f, ensure_ascii=False, indent=2)

print(f"\n✅ {len(new_samples)} new samples -> {path}")
