from docx import Document
import matplotlib.pyplot as plt
import os
import re

# Fungsi untuk memperbaiki rumus LaTeX
def fix_latex_formula(latex_formula):
    # Perbaiki kesalahan umum, seperti \cdotx -> \cdot x
    latex_formula = re.sub(r'\\cdot(\w)', r'\\cdot \1', latex_formula)  # Tambahkan spasi setelah \cdot
    return latex_formula

# Fungsi untuk merender rumus LaTeX ke gambar
def render_latex_to_image(latex_formula, output_path):
    try:
        # Perbaiki rumus sebelum dirender
        latex_formula = fix_latex_formula(latex_formula)

        # Ukuran gambar menyesuaikan panjang rumus
        fig_width = len(latex_formula) * 0.1  # Lebar gambar berdasarkan panjang rumus
        fig_height = 0.5  # Tinggi gambar
        plt.figure(figsize=(fig_width, fig_height))

        # Render rumus LaTeX
        plt.text(0.5, 0.5, f"${latex_formula}$", fontsize=12, ha='center', va='center')

        # Hilangkan axis dan padding
        plt.axis('off')
        plt.savefig(output_path, bbox_inches='tight', pad_inches=0, dpi=300)  # Tidak ada padding
        plt.close()
    except Exception as e:
        print(f"Gagal merender rumus: {latex_formula}. Error: {e}")

# Fungsi untuk konversi Word ke Markdown dengan rumus sebagai gambar
def convert_word_to_markdown(word_file, output_md, image_dir):
    # Buat direktori untuk gambar rumus
    os.makedirs(image_dir, exist_ok=True)

    # Buka dokumen Word
    doc = Document(word_file)
    markdown_content = []

    # Regex untuk mendeteksi rumus dalam format $ ... $
    formula_pattern = re.compile(r'\$(.*?)\$')

    # Loop melalui setiap paragraf di dokumen
    for i, paragraph in enumerate(doc.paragraphs):
        text = paragraph.text.strip()

        # Cek apakah paragraf adalah Heading
        if paragraph.style.name.startswith('Heading'):  # Cek style paragraf
            # Tentukan level Heading (1, 2, 3, dst.)
            heading_level = int(paragraph.style.name.split()[-1])  # Ambil angka dari nama style
            text = f"{'#' * heading_level} {text}"  # Format Markdown untuk Heading

        # Cek apakah paragraf adalah bagian dari daftar (list)
        elif paragraph.style.name.startswith('List'):  # Cek style paragraf
            if paragraph.style.name.startswith('List Bullet'):  # Bullet points
                text = f"- {text}"  # Format Markdown untuk bullet points
            elif paragraph.style.name.startswith('List Number'):  # Numbered lists
                text = f"1. {text}"  # Format Markdown untuk numbered lists

        # Cari semua rumus dalam paragraf
        formulas = formula_pattern.findall(text)

        # Jika ada rumus, proses satu per satu
        if formulas:
            for formula_index, formula in enumerate(formulas):  # Gunakan formula_index untuk reset indeks
                # Ekstrak rumus LaTeX (hilangkan delimiter $)
                latex_formula = formula

                # Validasi rumus
                if not latex_formula.strip():  # Jika rumus kosong, skip
                    print(f"Rumus kosong ditemukan di paragraf {i}, formula {formula_index}.")
                    continue

                # Render rumus ke gambar
                image_name = f"formula_{i}_{formula_index}.png"  # Gunakan formula_index untuk reset indeks
                image_path = os.path.join(image_dir, image_name)  # Path lengkap gambar
                render_latex_to_image(latex_formula, image_path)

                # Ganti rumus dengan referensi gambar di Markdown
                text = text.replace(f"${formula}$", f"![Rumus {i}_{formula_index}]({image_path})")

        # Tambahkan teks (yang sudah diproses) ke Markdown
        markdown_content.append(text)

    # Simpan konten Markdown ke file
    with open(output_md, "w", encoding="utf-8") as md_file:
        md_file.write("\n\n".join(markdown_content))

    print(f"File Markdown berhasil disimpan di: {output_md}")
    print(f"Gambar rumus disimpan di: {image_dir}")

# Contoh penggunaan
word_file = "document.docx"  # Ganti dengan path dokumen Word Anda
output_md = "output 2.md"  # File Markdown output
image_dir = "formula_images"  # Direktori untuk menyimpan gambar rumus

convert_word_to_markdown(word_file, output_md, image_dir)