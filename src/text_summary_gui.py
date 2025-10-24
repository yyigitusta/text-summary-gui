import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from transformers import pipeline
from textblob import TextBlob

# ---- ÖZETLEME MODELİ ----
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

# ---- GUI OLUŞTUR ----
root = tk.Tk()
root.title("Metin Özetleyici ve Duygu Analizi")
root.geometry("900x700")

# ---- TEXTBOXLAR ----
input_box = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=100, height=20)
input_box.pack(pady=10)

output_summary = tk.Text(root, height=10, width=100)
output_summary.pack(pady=10)

sentiment_label = tk.Label(root, text="Duygu Analizi: Henüz yapılmadı", font=("Arial", 12, "bold"))
sentiment_label.pack(pady=10)


# ---- METİN YÜKLEME ----
def load_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if file_path:
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()
        input_box.delete(1.0, tk.END)
        input_box.insert(tk.END, text)

# ---- ÖZETLEME ----
def summarize_text():
    text = input_box.get(1.0, tk.END).strip()
    if not text:
        messagebox.showwarning("Uyarı", "Lütfen metin gir veya dosya yükle.")
        return
    summary = summarizer(text, max_length=150, min_length=30, do_sample=False)[0]["summary_text"]
    output_summary.delete(1.0, tk.END)
    output_summary.insert(tk.END, summary)

    # ---- DUYGU ANALİZİ ----
    blob = TextBlob(text)
    sentiment = blob.sentiment.polarity
    if sentiment > 0.1:
        sentiment_label.config(text="Duygu Analizi: Pozitif 😊", fg="green")
    elif sentiment < -0.1:
        sentiment_label.config(text="Duygu Analizi: Negatif 😔", fg="red")
    else:
        sentiment_label.config(text="Duygu Analizi: Nötr 😐", fg="orange")


# ---- BUTONLAR ----
frame = tk.Frame(root)
frame.pack(pady=10)

btn_load = tk.Button(frame, text="📂 Dosya Yükle", command=load_file, width=20, bg="#4CAF50", fg="white")
btn_load.grid(row=0, column=0, padx=10)

btn_summarize = tk.Button(frame, text="🧠 Özetle + Analiz Et", command=summarize_text, width=20, bg="#2196F3", fg="white")
btn_summarize.grid(row=0, column=1, padx=10)

root.mainloop()
