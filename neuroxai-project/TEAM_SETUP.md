# 👥 دليل إعداد بيئة العمل لأعضاء الفريق

> اتبع هذه الخطوات بالترتيب في أول مرة تنزّل فيها المشروع على جهازك.

---

## الخطوة 1 — تثبيت Git (إذا لم يكن مثبتاً)

- **Windows:** [git-scm.com/download/win](https://git-scm.com/download/win)
- **Mac:** `brew install git`
- **Linux:** `sudo apt install git`

---

## الخطوة 2 — استنساخ المشروع

```bash
git clone https://github.com/YOUR_USERNAME/neuroxai-care.git
cd neuroxai-care
```

---

## الخطوة 3 — إنشاء بيئة Python افتراضية

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac / Linux
python3 -m venv venv
source venv/bin/activate
```

> يجب أن ترى `(venv)` في بداية السطر في الـ Terminal

---

## الخطوة 4 — تثبيت المكتبات

```bash
pip install -r requirements.txt
```

---

## الخطوة 5 — إعداد الملف السري

```bash
cp .env.example .env
```

افتح ملف `.env` وغيّر `FLASK_SECRET_KEY` لأي نص عشوائي طويل.

---

## الخطوة 6 — احصل على الملفات الحساسة من قائد الفريق

اطلب من قائد الفريق مشاركة هذه الملفات معك بشكل خاص (واتساب / إيميل):
- `DARWIN.csv` ← ضعه في جذر المشروع
- `artifacts/model_artifacts.pkl` ← ضعه داخل مجلد `artifacts/`
- `static/L.PNG` ← ضعه داخل مجلد `static/`

---

## الخطوة 7 — (اختياري) أعد تدريب النموذج

إذا لم تحصل على `model_artifacts.pkl`:

```bash
python train_model.py
```

---

## الخطوة 8 — تشغيل المشروع

```bash
python app.py
```

افتح: [http://localhost:5000](http://localhost:5000) ✅

---

## 🔄 روتين العمل اليومي

```bash
# قبل ما تبدأ أي تعديل — دائماً
git pull origin main

# بعد التعديل
git add .
git commit -m "وصف ما غيّرته"
git push origin main
```

---

## ❓ مشاكل شائعة

| المشكلة | الحل |
|---------|------|
| `ModuleNotFoundError` | تأكد أنك فعّلت الـ venv وشغّلت `pip install -r requirements.txt` |
| `FileNotFoundError: model_artifacts.pkl` | شغّل `python train_model.py` أو احصل على الملف من القائد |
| `git push` مرفوض | شغّل `git pull origin main` أولاً |
| الصفحة لا تفتح | تأكد أن التطبيق يعمل وافتح `http://localhost:5000` |
