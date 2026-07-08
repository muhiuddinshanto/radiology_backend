# Radiology Task & Annotation App - Backend

Django এবং Django REST Framework (DRF) দিয়ে তৈরি শক্তিশালী API সার্ভার।

## Core Features
- **JWT Authentication:** `simplejwt` ব্যবহার করে সুরক্ষিত API।
- **Models:** Task, UploadedImage, এবং AnnotationPolygon ডাটা সংরক্ষণের জন্য অপ্টিমাইজড মডেল।
- **SQLite Database:** সহজ ডেটা ম্যানেজমেন্টের জন্য ব্যবহৃত।

## Technical Details
- **Python Version:** 3.12+
- **Django Version:** 5.2

## How to Run
1. ভার্চুয়াল এনভায়রনমেন্ট তৈরি করুন: `python -m venv venv`
2. এনভায়রনমেন্ট অ্যাক্টিভেট করুন: `source venv/bin/activate` (Windows: `venv\Scripts\activate`)
3. ডিপেন্ডেন্সি ইনস্টল করুন: `pip install -r requirements.txt`
4. মাইগ্রেশন রান করুন: `python manage.py migrate`
5. সার্ভার স্টার্ট করুন: `python manage.py runserver`

## Deployment
প্রজেক্টটি `PythonAnywhere` বা `Render`-এ ডেপ্লয় করা হয়েছে। `DEBUG = False` মোডে সিকিউরিটি এনহ্যান্স করা হয়েছে।