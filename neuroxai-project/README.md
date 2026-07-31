# 🧠 NeuroXAI Care

> نظام دعم القرار السريري للكشف المبكر عن أمراض الجهاز العصبي عبر تحليل خط اليد باستخدام الذكاء الاصطناعي القابل للتفسير (XAI).

---

## 📋 متطلبات التشغيل

- Python 3.10 أو أحدث
- Git

---

## 🚀 إعداد المشروع (لأول مرة)

### 1. استنساخ المستودع

```bash
git clone https://github.com/YOUR_USERNAME/neuroxai-care.git
cd neuroxai-care
```

### 2. إنشاء بيئة افتراضية

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. تثبيت المكتبات

```bash
pip install -r requirements.txt
```

### 4. إعداد متغيرات البيئة

```bash
# انسخ ملف المثال
cp .env.example .env

# عدّل .env وغيّر FLASK_SECRET_KEY
```

### 5. إضافة الملفات المطلوبة (لا تُرفع على GitHub)

ضع الملفات التالية في المجلد الرئيسي للمشروع:
- `DARWIN.csv` — ملف البيانات
- `static/L.PNG` — شعار التطبيق

### 6. تدريب النموذج

```bash
python train_model.py
```

سيتم إنشاء ملف `artifacts/model_artifacts.pkl` تلقائياً.

### 7. تشغيل التطبيق

```bash
python app.py
```

افتح المتصفح على: [http://localhost:5000](http://localhost:5000)

---

## 📁 هيكل المشروع

```
neuroxai-care/
│
├── app.py                  # التطبيق الرئيسي (Flask)
├── train_model.py          # تدريب النموذج
├── requirements.txt        # مكتبات Python
├── .env.example            # مثال على متغيرات البيئة
├── .gitignore              # الملفات المستثناة من Git
│
├── templates/              # صفحات HTML
│   ├── login.html
│   ├── signup.html
│   ├── dashboard.html
│   ├── index.html          # صفحة التشخيص
│   ├── result.html
│   ├── patient_history.html
│   ├── patient_detail.html
│   ├── patient_login.html
│   ├── patient_dashboard.html
│   └── about.html
│
├── static/                 # ملفات CSS، صور، JS
│   ├── style.css
│   └── L.PNG               # ⚠️ أضفه يدوياً (غير مرفوع)
│
└── artifacts/              # مخرجات النموذج
    └── model_artifacts.pkl  # ⚠️ أنشئه بتشغيل train_model.py
```

---

## ⚠️ ملفات لا تُرفع على GitHub

الملفات التالية مدرجة في `.gitignore` لأسباب أمنية أو لحجمها:

| الملف | السبب |
|-------|-------|
| `DARWIN.csv` | بيانات حساسة / حجم كبير |
| `artifacts/model_artifacts.pkl` | ملف ضخم، يُنشأ بتشغيل `train_model.py` |
| `patients.db` | قاعدة بيانات المرضى |
| `users_auth.json` | بيانات تسجيل الدخول |
| `.env` | مفاتيح سرية |
| `static/L.PNG` | شعار المشروع (شاركه مع الفريق يدوياً) |

---

## 👥 سير عمل الفريق (Git Workflow)

### لكل عضو في الفريق — قبل أي تعديل:

```bash
git pull origin main
```

### بعد التعديل:

```bash
git add .
git commit -m "وصف التغيير بوضوح"
git push origin main
```

### إذا حصل تعارض (Conflict):

```bash
git pull origin main
# حل التعارض يدوياً في الملف
git add .
git commit -m "fix: حل تعارض الدمج"
git push origin main
```

---

## 🌐 النشر على Render (مجاني)

1. ارفع المشروع على GitHub
2. اذهب إلى [render.com](https://render.com) وأنشئ حساباً
3. اختر **New Web Service** واربطه بالمستودع
4. اضبط هذه الإعدادات:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`
5. أضف متغيرات البيئة من `.env.example` في قسم Environment
6. ⚠️ ستحتاج لرفع `model_artifacts.pkl` بطريقة بديلة (انظر ملاحظة أدناه)

> **ملاحظة:** ملف النموذج كبير، يمكن استخدام [Git LFS](https://git-lfs.github.com/) أو تخزينه في خدمة مثل Google Drive وتحميله عند بدء التشغيل.

---

## 🤝 المساهمة

1. لا تعدّل مباشرة على `main` إذا كنتم فريقاً — استخدموا branches:
   ```bash
   git checkout -b feature/اسم-الميزة
   # بعد الانتهاء
   git push origin feature/اسم-الميزة
   # ثم افتح Pull Request على GitHub
   ```

2. اكتب commit messages واضحة بالعربي أو الإنجليزي
3. لا ترفع ملفات حساسة أبداً

---

## 📞 الدعم

للتواصل مع فريق الدعم: support@neuroxai.care
