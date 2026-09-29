# 01 - Mẹ Yêu Của Con

| Mục | Chọn |
|---|---|
| Thể loại | Trữ tình, bolero (slow rumba), 72 bpm |
| Giọng | Nữ, giọng Nam, ngân rung (vibrato) |
| Ca sĩ | Ca sĩ AI hư cấu (chưa có ảnh chân dung), mô tả cố định trong `prompts.md` |
| Bối cảnh | Phòng trà Sài Gòn ánh vàng hổ phách, xen 2 cảnh minh họa hiên nhà quê lúc chiều |
| Nhạc cụ | Guitar cổ điển, dây nền |
| Tỷ lệ | 9:16 (1080x1920) |
| Độ dài | 60 giây, 11 cảnh (3 cảnh nhép miệng, 5 cảnh Flow, 3 ảnh tĩnh) |

## Lời (lục bát, lời mới hoàn toàn)

```
[Intro]

[Verse]
Chiều quê gió thổi hiên nhà
Mẹ ngồi vá áo bên tà nắng phai
Mái đầu sương điểm hôm mai
Một đời mẹ gánh chông gai nhọc nhằn

[Chorus]
Mẹ yêu, mẹ của đời con
Tình như biển rộng, như non ngút ngàn
Mẹ yêu, mẹ của đời con
Con đi muôn dặm, lòng son nhớ về

[Outro]
(Mẹ ơi, mẹ ơi...)
```

Ghi chú thanh điệu: mọi chữ cuối câu đều thanh bằng (nhà, phai, mai, nhằn, con, ngàn, về). Câu móc "Mẹ yêu, mẹ của đời con" lặp 2 lần, chứa tên bài. Chữ "mẹ" (thanh nặng) AI có thể hát thành "me": nghe bản Suno, nếu sai ở câu móc thì tạo lại.

## Suno

- **Title:** `Mẹ Yêu Của Con`
- **Style** (177 ký tự):
  `Vietnamese bolero, 72 bpm, classical guitar, slow rumba rhythm, soft strings, soulful female vocal with vibrato, southern Vietnamese accent, tender, nostalgic, Vietnamese lyrics`
- **Exclude:** `english lyrics, spoken word, heavy autotune, rap, electronic drums`

72 bpm: 1 ô nhịp ≈ 3,33 giây. Mỗi câu lục bát ≈ 2 ô nhịp ≈ 6,67 giây. Mốc bên dưới là ước lượng, bước 6 chỉnh theo nhạc thật.

## Bảng cảnh

| Cảnh | Giây | Loại | Cỡ cảnh, góc máy | Hành động | Câu hát | Nguồn |
|---|---|---|---|---|---|---|
| 01 | 0 tới 6,7 | không hát | Toàn cảnh phòng trà | Đèn spotlight bật lên, ca sĩ ngồi ghế cao ôm đàn | (Intro, tiêu đề 3 giây) | Gemini + Flow |
| 02 | 6,7 tới 10 | không hát | Toàn cảnh, minh họa | Hiên nhà quê chiều, gió lay hàng cau, rèm tre | Chiều quê gió thổi hiên nhà | Gemini + Flow |
| 03 | 10 tới 13,3 | không hát | Trung cảnh nghiêng 3/4, ngược sáng | Ca sĩ nhắm mắt, đàn nhẹ | (tiếp câu 1) | Ảnh tĩnh, zoom_out |
| 04 | 13,3 tới 20 | không hát | Trung cảnh, minh họa | Người mẹ tóc bạc ngồi vá áo bên hiên, nắng chiều | Mẹ ngồi vá áo bên tà nắng phai | Gemini + Flow |
| 05 | 20 tới 26,7 | **hát** | Cận mặt, nhìn thẳng | Ca sĩ hát, mắt ngấn nước | Mái đầu sương điểm hôm mai | Gemini + nhép miệng |
| 06 | 26,7 tới 30 | không hát | Qua vai khán giả | Bàn tròn, nến, ca sĩ trên sân khấu xa | Một đời mẹ gánh... | Ảnh tĩnh, pan_phai |
| 07 | 30 tới 33,3 | không hát | Cận tay đàn, mờ nhẹ | Tay trên dây đàn, bokeh vàng | ...chông gai nhọc nhằn | Ảnh tĩnh, zoom_in |
| 08 | 33,3 tới 40 | **hát** | Trung cận, nhìn thẳng | Hát câu móc, micro đứng dưới cằm | Mẹ yêu, mẹ của đời con | Gemini + nhép miệng |
| 09 | 40 tới 46,7 | không hát | Toàn cảnh, máy lia quanh | Khán giả lặng nghe, ánh nến, có người lau nước mắt | Tình như biển rộng, như non ngút ngàn | Gemini + Flow |
| 10 | 46,7 tới 53,3 | **hát** | Cận mặt | Hát lặp câu móc, giọt nước mắt | Mẹ yêu, mẹ của đời con | Gemini + nhép miệng |
| 11 | 53,3 tới 60 | không hát | Toàn cảnh xa | Ca sĩ cúi đầu, đèn tắt dần | Con đi muôn dặm, lòng son nhớ về | Gemini + Flow |

Credit dự kiến: Flow 5 clip ≈ 25 credit (1 ngày). Nhép miệng 3 cảnh: Dreamina trước; nếu phải dùng Kling (1 cảnh/ngày) thì mất 3 ngày, hoặc chuyển cảnh 05 sang ảnh tĩnh.

Lưu ý: bolero Suno hay có intro dài hơn 6,7 giây. Nếu vậy thì dời mốc các cảnh, hoặc đặt `nhac_bat_dau` vào chỗ bắt đầu hát trừ khoảng 5 giây. Nếu câu cuối điệp khúc rơi sau giây 60 thì tăng `do_dai` (và `ket_thuc` cảnh 11) cho trọn câu.
