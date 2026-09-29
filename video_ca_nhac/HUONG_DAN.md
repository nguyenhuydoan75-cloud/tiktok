# Video ca nhạc AI: làm tiếp trên máy

Chép cả thư mục `video_ca_nhac` vào `D:\COWORKAI\Ke_hoach_video_ca_nhac_AI (Đoàn)` (gộp với `02_du_an`, `03_thanh_pham`, `cong_cu` sẵn có). Nếu nhật ký đã có bài số 01 thì đổi số dự án và `"so"` trong `du_an.json`.

Bài 01 - Mẹ Yêu Của Con đã xong bước 1 (lời, Suno style, bảng cảnh, prompt, `du_an.json`, phụ đề ước lượng, caption). Còn lại:

1. Suno: dán lời, style, tên bài trong `kich_ban.md`, nghe chọn bản, lưu `nhac/bai_hat.mp3`.
2. Gemini: sinh 11 ảnh theo `prompts.md`, lưu `anh/canhNN.png`.
3. `python3 dung_video.py chuan_bi "../02_du_an/01 - Mẹ Yêu Của Con"` để cắt giọng cho cảnh 05, 08, 10.
4. Flow cho cảnh 01, 02, 04, 09, 11; Dreamina hoặc Kling nhép miệng cho 05, 08, 10. Lưu `clip/canhNN.mp4`.
5. Chỉnh `phu_de.srt` theo nhạc thật, rồi `kiem_tra`, `dung`, `nghiem_thu`.

Hoặc mở Cowork trên máy và nói "làm tiếp video ca nhạc Mẹ Yêu Của Con".
