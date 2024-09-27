import tkinter as tk
from tkinter import messagebox, filedialog
from yt_dlp import YoutubeDL
import os
import sys

def download_videos():
    raw_input = text_input.get("1.0", tk.END).strip()
    folder_name = folder_name_input.get().strip()
    download_dir = download_dir_input.get().strip()

    if not raw_input:
        messagebox.showwarning("Cảnh báo", "Vui lòng nhập ít nhất một đường link.")
        return

    if not folder_name:
        messagebox.showwarning("Cảnh báo", "Vui lòng nhập tên thư mục.")
        return

    if not download_dir:
        messagebox.showwarning("Cảnh báo", "Vui lòng chọn đường dẫn lưu trữ.")
        return

    # Tạo đường dẫn lưu trữ đầy đủ
    full_path = os.path.join(download_dir, folder_name)

    # Tạo thư mục nếu chưa tồn tại
    if not os.path.exists(full_path):
        os.makedirs(full_path)

    # Xử lý các đường link
    urls = raw_input.split('\n')
    total_links = len(urls)
    unique_urls = set()
    duplicate_urls = []
    downloaded_urls = []
    failed_urls = []  # Danh sách các link tải không thành công

    # Hiển thị cửa sổ tiến độ
    progress_window = tk.Toplevel(root)
    progress_window.title("Tiến độ tải video")

    progress_label = tk.Label(progress_window, text="Đang chuẩn bị tải...")
    progress_label.pack(pady=10, padx=10)

    root.update()

    # Tùy chọn cho yt-dlp
    ydl_opts = {
        'outtmpl': os.path.join(full_path, '%(title)s.%(ext)s'),
        'format': 'best',
        'quiet': True,
    }

    downloaded_count = 0  # Số lượng link đã tải thành công

    with YoutubeDL(ydl_opts) as ydl:
        for index, url in enumerate(urls, start=1):
            url = url.strip()
            if url:
                # Loại bỏ số thứ tự và dấu gạch ngang nếu có
                if '-' in url:
                    url = url.split('-', 1)[1].strip()
                # Kiểm tra xem đường link đã được xử lý chưa
                if url not in unique_urls:
                    unique_urls.add(url)
                    progress_label.config(text=f"Đang tải link {index}/{total_links}  ")
                    root.update_idletasks()
                    try:
                        ydl.download([url])
                        downloaded_urls.append(url)
                        downloaded_count += 1
                    except Exception as e:
                        failed_urls.append(url)
                    progress_label.config(text=f"Đã tải {downloaded_count}/{total_links} link")
                    root.update_idletasks()
                else:
                    duplicate_urls.append(url)
            else:
                total_links -= 1  # Giảm tổng số link nếu dòng trống

    progress_window.destroy()

    # Hiển thị kết quả trong cửa sổ mới
    result_window = tk.Toplevel(root)
    result_window.title("Kết quả tải video")

    # Tạo khung chứa các thông báo
    frame = tk.Frame(result_window)
    frame.pack(pady=10, padx=10)

    # Hiển thị thông báo tải thành công
    if downloaded_urls:
        success_label = tk.Label(frame, text="Các link đã tải thành công:")
        success_label.pack(anchor='w')
        for link in downloaded_urls:
            link_label = tk.Label(frame, text=link)
            link_label.pack(anchor='w')

    # Hiển thị thông báo link trùng lặp
    if duplicate_urls:
        duplicate_label = tk.Label(frame, text="Các link trùng lặp (không tải lại):")
        duplicate_label.pack(anchor='w', pady=(10, 0))
        for link in duplicate_urls:
            link_label = tk.Label(frame, text=link)
            link_label.pack(anchor='w')

    # Hiển thị các link tải không thành công với màu đỏ và nút Copy
    if failed_urls:
        failed_label = tk.Label(frame, text="Không thành công:", fg="red")
        failed_label.pack(anchor='w', pady=(10, 0))

        for link in failed_urls:
            link_frame = tk.Frame(frame)
            link_frame.pack(anchor='w')

            link_label = tk.Label(link_frame, text=link, fg="red")
            link_label.pack(side=tk.LEFT)

            copy_button = tk.Button(link_frame, text="Copy", command=lambda l=link: copy_to_clipboard(l))
            copy_button.pack(side=tk.LEFT, padx=5)
    else:
        no_fail_label = tk.Label(frame, text="Tất cả các video đều được tải thành công!")
        no_fail_label.pack(anchor='w', pady=(10, 0))

    # Nút đóng cửa sổ
    close_button = tk.Button(result_window, text="Đóng", command=result_window.destroy)
    close_button.pack(pady=5)

def copy_to_clipboard(text):
    root.clipboard_clear()
    root.clipboard_append(text)
 #   messagebox.showinfo("Thông báo", f"Đã sao chép link:\n{text}")

def browse_folder():
    folder_selected = filedialog.askdirectory(initialdir=os.path.join(os.path.expanduser("~"), "Downloads"))
    if folder_selected:
        download_dir_input.delete(0, tk.END)
        download_dir_input.insert(0, folder_selected)

# Tạo cửa sổ chính
root = tk.Tk()
root.title("S-Downloader - Ver1")

# Thêm icon cho ứng dụng
if sys.platform.startswith('win'):
    if os.path.exists('app_icon.ico'):
        root.iconbitmap('app_icon.ico')
else:
    if os.path.exists('app_icon.png'):
        icon_image = tk.PhotoImage(file='app_icon.png')
        root.iconphoto(False, icon_image)

# Tạo khung nhập liệu đường link
label = tk.Label(root, text="Nhập các đường link video TikTok (mỗi link trên một dòng):")
label.pack(pady=10)

text_input = tk.Text(root, height=5, width=40)
text_input.pack(pady=5)

# Tạo khung nhập tên thư mục
folder_name_label = tk.Label(root, text="Nhập tên thư mục:")
folder_name_label.pack(pady=5)

folder_name_input = tk.Entry(root, width=50)
folder_name_input.pack(pady=5)

# Tạo khung chọn đường dẫn lưu trữ
download_dir_frame = tk.Frame(root)
download_dir_frame.pack(pady=5)

download_dir_label = tk.Label(download_dir_frame, text="Lưu trữ:")
download_dir_label.pack(side=tk.LEFT, padx=5)

download_dir_input = tk.Entry(download_dir_frame, width=40)
download_dir_input.pack(side=tk.LEFT, padx=5)

# Đặt giá trị mặc định cho ô nhập đường dẫn lưu trữ
default_download_dir = os.path.join(os.path.expanduser("~"), "Downloads")
download_dir_input.insert(0, default_download_dir)

browse_button = tk.Button(download_dir_frame, text="Duyệt...", command=browse_folder)
browse_button.pack(side=tk.LEFT, padx=5)

# Nút tải video
download_button = tk.Button(root, text="Tải Video", command=download_videos)
download_button.pack(pady=10)

# Chạy ứng dụng
root.mainloop()
