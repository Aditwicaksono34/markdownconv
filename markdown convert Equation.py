import matplotlib.pyplot as plt
import os
import re

# Atur font family dan font serif
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Times New Roman']
plt.rcParams['font.size'] = 12

# Fungsi untuk memperbaiki rumus LaTeX
def fix_latex_formula(latex_formula):
    # Perbaiki kesalahan umum, seperti \cdotx -> \cdot x
    latex_formula = re.sub(r'\\cdot(\w)', r'\\cdot \1', latex_formula)  # Tambahkan spasi setelah \cdot
    return latex_formula

# Fungsi untuk merender rumus LaTeX ke gambar
def render_latex_to_image(latex_formula, output_path, is_block=False):
    try:
        # Perbaiki rumus sebelum dirender
        latex_formula = fix_latex_formula(latex_formula)

        # Ukuran gambar menyesuaikan panjang rumus
        fig_width = len(latex_formula) * 0.1  # Lebar gambar berdasarkan panjang rumus
        fig_height = 0.5 if not is_block else 0.7  # Tinggi gambar lebih besar untuk rumus block

        # Buat figure dengan latar belakang transparan
        fig = plt.figure(figsize=(fig_width, fig_height), dpi=300, facecolor='none')
        ax = fig.add_axes([0, 0, 1, 1], frameon=False)  # Tambahkan axes tanpa frame
        ax.set_xticks([])  # Hilangkan ticks sumbu x
        ax.set_yticks([])  # Hilangkan ticks sumbu y

        # Render rumus LaTeX dengan font Times New Roman
        ax.text(0.5, 0.5, f"${latex_formula}$" if not is_block else f"${latex_formula}$", 
                fontsize=12, ha='center', va='center', fontname='Times New Roman')

        # Hilangkan axis dan padding
        plt.axis('off')

        # Simpan gambar dengan latar belakang transparan
        plt.savefig(output_path, bbox_inches='tight', pad_inches=0, dpi=300, transparent=True)
        plt.close()
    except Exception as e:
        print(f"Gagal merender rumus: {latex_formula}. Error: {e}")


# Fungsi untuk mengonversi rumus di Markdown ke gambar dan memasukkannya kembali
def convert_markdown_formulas_to_images(markdown_file, output_md, image_dir):
    # Buat direktori untuk gambar rumus
    os.makedirs(image_dir, exist_ok=True)

    # Baca file Markdown
    with open(markdown_file, "r", encoding="utf-8") as md_file:
        markdown_content = md_file.read()

    # Regex untuk mendeteksi rumus block (\[ ... \]), inline (\( ... \)), dan rumus dalam kurung siku ([ ... ])
    block_formula_pattern = re.compile(r'\\\[(.*?)\\\]')  # Deteksi rumus block
    inline_formula_pattern = re.compile(r'\\\((.*?)\\\)')  # Deteksi rumus inline
    square_bracket_formula_pattern = re.compile(r'\[(.*?)\]')  # Deteksi rumus dalam kurung siku
    dollar_bracket_formula_pattern = re.compile(r'\$(.*?)\$')  # Deteksi rumus dalam dollar

    # Temukan semua rumus block dalam file Markdown
    block_formulas = block_formula_pattern.findall(markdown_content)
    # Temukan semua rumus inline dalam file Markdown
    inline_formulas = inline_formula_pattern.findall(markdown_content)
    # Temukan semua rumus dalam kurung siku dalam file Markdown
    square_bracket_formulas = square_bracket_formula_pattern.findall(markdown_content)
    # Temukan semua rumus dalam dollar dalam file Markdown
    dollar_bracket_formulas = dollar_bracket_formula_pattern.findall(markdown_content)

    # Proses rumus block
    for formula_index, formula in enumerate(block_formulas):
        # Render rumus ke gambar
        image_name = f"block_formula_{formula_index}.png"  # Nama file gambar
        image_path = os.path.join(image_dir, image_name)  # Path lengkap gambar
        render_latex_to_image(formula, image_path, is_block=True)

        # Ganti rumus block dengan referensi gambar di Markdown
        markdown_content = markdown_content.replace(
            f"\\[{formula}\\]", f"![Rumus Block {formula_index}]({image_path})", 1
        )

    # Proses rumus inline
    for formula_index, formula in enumerate(inline_formulas):
        # Render rumus ke gambar
        image_name = f"inline_formula_{formula_index}.png"  # Nama file gambar
        image_path = os.path.join(image_dir, image_name)  # Path lengkap gambar
        render_latex_to_image(formula, image_path, is_block=False)

        # Ganti rumus inline dengan referensi gambar di Markdown
        markdown_content = markdown_content.replace(
            f"\\({formula}\\)", f"![Rumus Inline {formula_index}]({image_path})", 1
        )

    # Proses rumus dalam kurung siku
    for formula_index, formula in enumerate(square_bracket_formulas):
        # Render rumus ke gambar
        image_name = f"square_bracket_formula_{formula_index}.png"  # Nama file gambar
        image_path = os.path.join(image_dir, image_name)  # Path lengkap gambar
        render_latex_to_image(formula, image_path, is_block=True)

        # Ganti rumus dalam kurung siku dengan referensi gambar di Markdown
        markdown_content = markdown_content.replace(
            f"[{formula}]", f"![Rumus Kurung Siku {formula_index}]({image_path})", 1
        )

    # Proses rumus dalam dollar
    for formula_index, formula in enumerate(dollar_bracket_formulas):
        # Render rumus ke gambar
        image_name = f"dollar_bracket_formula_{formula_index}.png"  # Nama file gambar
        image_path = os.path.join(image_dir, image_name)  # Path lengkap gambar
        render_latex_to_image(formula, image_path, is_block=False)

        # Ganti rumus dalam dollar dengan referensi gambar di Markdown
        markdown_content = markdown_content.replace(
            f"${formula}$", f"![Rumus Dollar {formula_index}]({image_path})", 1
        )

    # Simpan konten Markdown yang sudah diproses ke file
    with open(output_md, "w", encoding="utf-8") as md_file:
        md_file.write(markdown_content)

    print(f"File Markdown berhasil disimpan di: {output_md}")
    print(f"Gambar rumus disimpan di: {image_dir}")

# Contoh penggunaan
markdown_file = "input.md"  # Ganti dengan path file Markdown 
output_md = "output.md"  # File Markdown output
image_dir = "formula_images"  # Direktori untuk menyimpan gambar rumus

convert_markdown_formulas_to_images(markdown_file, output_md, image_dir)