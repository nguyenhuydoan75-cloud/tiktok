#!/usr/bin/env python3
"""Dựng video ca nhạc từ du_an.json trong một thư mục dự án.

Cách chạy (trong máy ảo, thư mục dự án chứa du_an.json):
    python3 dung_video.py chuan_bi  <thu_muc_du_an>   # tạo thư mục con, cắt đoạn giọng cho cảnh hát
    python3 dung_video.py kiem_tra  <thu_muc_du_an>   # liệt kê file còn thiếu
    python3 dung_video.py dung      <thu_muc_du_an>   # dựng video, gọi lại tới khi in XONG
    python3 dung_video.py nghiem_thu <thu_muc_du_an>  # ảnh 6 khung để kiểm tra

Lệnh "dung" có hạn giờ (HAN_GIO giây). Hết giờ mà chưa xong thì in "CHUA XONG, goi lai":
các cảnh đã dựng được giữ trong thư mục _tam nên lần gọi sau chạy tiếp.
Biến môi trường: FFMPEG (đường dẫn ffmpeg), HAN_GIO (mặc định 120), FONT (mặc định Liberation Sans).
"""
import json, os, re, subprocess, sys, time

FFMPEG = os.environ.get("FFMPEG", "ffmpeg")
HAN_GIO = float(os.environ.get("HAN_GIO", "120"))
FONT = os.environ.get("FONT", "Liberation Sans")
BAT_DAU = time.time()

KICH_THUOC = {"9:16": (1080, 1920), "16:9": (1920, 1080), "1:1": (1080, 1080), "4:5": (1080, 1350)}
DUOI_ANH = (".png", ".jpg", ".jpeg", ".webp")


def doc_du_an(thu_muc):
    with open(os.path.join(thu_muc, "du_an.json"), encoding="utf-8") as f:
        da = json.load(f)
    da.setdefault("fps", 30)
    da.setdefault("nhac_bat_dau", 0.0)
    da.setdefault("fade", 0.25)
    if da["ty_le"] not in KICH_THUOC:
        sys.exit(f"ty_le phai la mot trong {list(KICH_THUOC)}")
    da["W"], da["H"] = KICH_THUOC[da["ty_le"]]
    return da


def chay(lenh):
    kq = subprocess.run(lenh, capture_output=True, text=True)
    if kq.returncode != 0:
        print(" ".join(lenh))
        print(kq.stderr[-2500:])
        sys.exit("LOI ffmpeg")


def het_gio():
    return time.time() - BAT_DAU > HAN_GIO


def do_dai(canh):
    return round(float(canh["ket_thuc"]) - float(canh["bat_dau"]), 3)


# ---------------- chuan_bi ----------------
def chuan_bi(thu_muc, da):
    for con in ("nhac", "anh", "clip", "am_thanh_hat", "_tam"):
        os.makedirs(os.path.join(thu_muc, con), exist_ok=True)
    nhac = os.path.join(thu_muc, da["nhac"])
    if not os.path.exists(nhac):
        print(f"Chua co file nhac {da['nhac']}. Bo nhac vao roi chay lai chuan_bi de cat giong cho canh hat.")
        return
    for c in da["canh"]:
        if c.get("loai") != "hat":
            continue
        ra = os.path.join(thu_muc, "am_thanh_hat", f"canh{int(c['so']):02d}.mp3")
        tu = float(da["nhac_bat_dau"]) + float(c["bat_dau"])
        chay([FFMPEG, "-y", "-ss", f"{tu:.3f}", "-t", f"{do_dai(c):.3f}", "-i", nhac,
              "-ac", "2", "-ar", "44100", "-b:a", "192k", ra])
        print(f"canh {c['so']:>2}: {os.path.relpath(ra, thu_muc)}  ({do_dai(c)} giay, tu giay {tu:.2f} cua bai)")
    print("XONG chuan_bi")


# ---------------- kiem_tra ----------------
def kiem_tra(thu_muc, da, in_ra=True):
    thieu = []
    if not os.path.exists(os.path.join(thu_muc, da["nhac"])):
        thieu.append(da["nhac"])
    truoc = 0.0
    for c in da["canh"]:
        if not os.path.exists(os.path.join(thu_muc, c["file"])):
            thieu.append(f"canh {c['so']}: {c['file']}")
        if abs(float(c["bat_dau"]) - truoc) > 0.01:
            thieu.append(f"canh {c['so']}: bat_dau {c['bat_dau']} khong noi tiep canh truoc ({truoc})")
        truoc = float(c["ket_thuc"])
    if abs(truoc - float(da["do_dai"])) > 0.05:
        thieu.append(f"canh cuoi ket thuc o {truoc}, khac do_dai {da['do_dai']}")
    if da.get("phu_de") and not os.path.exists(os.path.join(thu_muc, da["phu_de"])):
        thieu.append(da["phu_de"])
    if in_ra:
        print("DU FILE" if not thieu else "THIEU / SAI:\n  " + "\n  ".join(thieu))
    return thieu


# ---------------- dung ----------------
def loc_phu_kin(da, cat_day):
    """Phóng ảnh/clip cho kín khung rồi cắt giữa; cat_day bỏ phần đáy (logo Gemini)."""
    W, H = da["W"], da["H"]
    truoc = f"crop=iw:ih*{1 - cat_day:.3f}:0:0," if cat_day else ""
    return f"{truoc}scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},setsar=1"


def dung_canh(thu_muc, da, c, ra):
    W, H, fps = da["W"], da["H"], da["fps"]
    d = do_dai(c)
    vao = os.path.join(thu_muc, c["file"])
    cat_day = float(c.get("cat_day", 0))
    fade = min(float(da["fade"]), d / 4)
    mo = f"fade=t=in:st=0:d={fade},fade=t=out:st={d - fade:.3f}:d={fade}"
    if vao.lower().endswith(DUOI_ANH):
        n = int(round(d * fps))
        kieu = c.get("chuyen_dong", "zoom_in")
        z = {"zoom_in": "1+0.10*on/{n}", "zoom_out": "1.10-0.10*on/{n}"}.get(kieu, "1.08").format(n=n)
        x = {"pan_trai": "(iw-iw/zoom)*(1-on/{n})", "pan_phai": "(iw-iw/zoom)*on/{n}"}.get(kieu, "(iw-iw/zoom)/2").format(n=n)
        loc = (f"{loc_phu_kin(da, cat_day)},scale={W * 2}:{H * 2},"
               f"zoompan=z='{z}':x='{x}':y='(ih-ih/zoom)/2':d={n}:s={W}x{H}:fps={fps},{mo}")
        lenh = [FFMPEG, "-y", "-loop", "1", "-framerate", str(fps), "-t", f"{d:.3f}", "-i", vao]
    else:
        # Cảnh hát không được lặp (sẽ lệch khẩu hình): thiếu thì giữ khung cuối. Cảnh khác thì lặp cho đủ.
        lap = [] if c.get("loai") == "hat" else ["-stream_loop", "-1"]
        loc = f"fps={fps},{loc_phu_kin(da, cat_day)},tpad=stop_mode=clone:stop_duration={d:.3f},{mo}"
        lenh = [FFMPEG, "-y", *lap, "-i", vao]
    chay(lenh + ["-t", f"{d:.3f}", "-vf", loc, "-an", "-c:v", "libx264", "-preset", "veryfast",
                 "-crf", "18", "-pix_fmt", "yuv420p", "-r", str(fps), ra])


def giay_srt(s):
    h, m, rest = s.strip().replace(".", ",").split(":")
    giay, ms = rest.split(",")
    return int(h) * 3600 + int(m) * 60 + int(giay) + int(ms) / 1000


def giay_ass(t):
    t = max(t, 0)
    return f"{int(t // 3600)}:{int(t % 3600 // 60):02d}:{t % 60:05.2f}"


def tao_ass(thu_muc, da, ra):
    W, H = da["W"], da["H"]
    doc = W < H
    co_chu = 64 if doc else 58
    le_duoi = int(H * (0.16 if doc else 0.08))
    dong = [
        "[Script Info]", "ScriptType: v4.00+", f"PlayResX: {W}", f"PlayResY: {H}", "WrapStyle: 0", "",
        "[V4+ Styles]",
        "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, "
        "Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding",
        f"Style: Loi,{FONT},{co_chu},&H00FFFFFF,&H0000D7FF,&H00000000,&H64000000,1,0,0,0,100,100,0,0,1,4,2,2,80,80,{le_duoi},1",
        f"Style: TieuDe,{FONT},{int(co_chu * 1.7)},&H0000D7FF,&H00FFFFFF,&H00000000,&H64000000,1,0,0,0,100,100,2,0,1,6,3,5,60,60,0,1",
        f"Style: Phu,{FONT},{int(co_chu * 0.8)},&H00FFFFFF,&H00FFFFFF,&H00000000,&H64000000,0,1,0,0,100,100,1,0,1,3,2,5,60,60,0,1",
        f"Style: Logo,{FONT},{int(co_chu * 0.6)},&H80FFFFFF,&H00FFFFFF,&H80000000,&H00000000,1,0,0,0,100,100,1,0,1,2,0,9,40,40,40,1",
        "", "[Events]", "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text",
    ]
    tong = float(da["do_dai"])
    td = da.get("tieu_de_mo_dau")
    het_tieu_de = 0.0
    if td and td.get("chu"):
        g = float(td.get("giay", 3))
        het_tieu_de = g
        y = H * 0.42
        dong.append(f"Dialogue: 2,{giay_ass(0.2)},{giay_ass(g)},TieuDe,,0,0,0,,{{\\fad(400,500)\\pos({W // 2},{int(y)})}}{td['chu']}")
        if td.get("phu"):
            dong.append(f"Dialogue: 2,{giay_ass(0.6)},{giay_ass(g)},Phu,,0,0,0,,{{\\fad(400,500)\\pos({W // 2},{int(y + co_chu * 1.9)})}}{td['phu']}")
    if da.get("logo_chu"):
        dong.append(f"Dialogue: 1,{giay_ass(0)},{giay_ass(tong)},Logo,,0,0,0,,{da['logo_chu']}")
    if da.get("phu_de"):
        with open(os.path.join(thu_muc, da["phu_de"]), encoding="utf-8-sig") as f:
            khoi = re.split(r"\n\s*\n", f.read().strip())
        for k in khoi:
            dong_k = [x for x in k.splitlines() if x.strip()]
            moc = next((x for x in dong_k if "-->" in x), None)
            if not moc:
                continue
            a, b = (giay_srt(x) for x in moc.split("-->"))
            a = max(a, het_tieu_de)  # lời không đè lên tiêu đề mở đầu
            if a >= b:
                continue
            chu = r"\N".join(x for x in dong_k[dong_k.index(moc) + 1:])
            dong.append(f"Dialogue: 0,{giay_ass(a)},{giay_ass(min(b, tong))},Loi,,0,0,0,,{{\\fad(150,150)}}{chu}")
    with open(ra, "w", encoding="utf-8") as f:
        f.write("\n".join(dong) + "\n")


def ten_thanh_pham(da):
    so = f"{int(da['so']):02d} - " if da.get("so") is not None else ""
    return f"{so}{da['ten_bai']} ({da['ty_le'].replace(':', 'x')}).mp4"


def dung(thu_muc, da):
    thieu = kiem_tra(thu_muc, da, in_ra=False)
    if thieu:
        print("THIEU / SAI:\n  " + "\n  ".join(thieu))
        sys.exit("Chua dung duoc")
    tam = os.path.join(thu_muc, "_tam")
    os.makedirs(tam, exist_ok=True)
    doan = []
    for c in da["canh"]:
        ra = os.path.join(tam, f"canh{int(c['so']):02d}.mp4")
        doan.append(ra)
        if os.path.exists(ra) and os.path.getsize(ra) > 1000:
            continue
        if het_gio():
            print("CHUA XONG, goi lai")
            return
        dung_canh(thu_muc, da, c, ra + ".tmp.mp4")
        os.replace(ra + ".tmp.mp4", ra)
        print(f"da dung canh {c['so']}")
    if het_gio():
        print("CHUA XONG, goi lai")
        return
    ds = os.path.join(tam, "ds.txt")
    with open(ds, "w", encoding="utf-8") as f:
        f.writelines(f"file '{os.path.basename(p)}'\n" for p in doan)
    hinh = os.path.join(tam, "hinh.mp4")
    chay([FFMPEG, "-y", "-f", "concat", "-safe", "0", "-i", ds, "-c", "copy", hinh])
    ass = os.path.join(tam, "chu.ass")
    tao_ass(thu_muc, da, ass)
    d = float(da["do_dai"])
    am = (f"afade=t=in:st=0:d=0.6,afade=t=out:st={max(d - 2, 0):.2f}:d=2,"
          f"loudnorm=I=-14:TP=-1:LRA=11")
    thanh_pham = da.get("thu_muc_thanh_pham") or thu_muc
    thanh_pham = os.path.normpath(os.path.join(thu_muc, thanh_pham))
    os.makedirs(thanh_pham, exist_ok=True)
    ra = os.path.join(thanh_pham, ten_thanh_pham(da))
    ass_loc = ass.replace("\\", "/").replace(":", "\\:").replace("'", "\\'")
    chay([FFMPEG, "-y", "-i", hinh, "-ss", f"{float(da['nhac_bat_dau']):.3f}", "-t", f"{d:.3f}",
          "-i", os.path.join(thu_muc, da["nhac"]),
          "-map", "0:v", "-map", "1:a", "-vf", f"ass='{ass_loc}'", "-af", am,
          "-c:v", "libx264", "-preset", "medium", "-crf", "19", "-pix_fmt", "yuv420p",
          "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart", "-t", f"{d:.3f}", ra])
    print(f"XONG {ra}")


# ---------------- nghiem_thu ----------------
def nghiem_thu(thu_muc, da):
    thanh_pham = os.path.normpath(os.path.join(thu_muc, da.get("thu_muc_thanh_pham") or "."))
    vao = os.path.join(thanh_pham, ten_thanh_pham(da))
    if not os.path.exists(vao):
        sys.exit(f"Chua co video {vao}")
    d = float(da["do_dai"])
    ra = os.path.join(thu_muc, "nghiem_thu.jpg")
    rong = 300 if da["W"] < da["H"] else 480
    chay([FFMPEG, "-y", "-i", vao, "-vf", f"fps=6/{d:.2f},scale={rong}:-2,tile=3x2", "-frames:v", "1", "-q:v", "4", ra])
    print(f"XONG {ra}")


if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[1] not in ("chuan_bi", "kiem_tra", "dung", "nghiem_thu"):
        sys.exit(__doc__)
    tm = os.path.abspath(sys.argv[2])
    du_an = doc_du_an(tm)
    {"chuan_bi": chuan_bi, "kiem_tra": kiem_tra, "dung": dung, "nghiem_thu": nghiem_thu}[sys.argv[1]](tm, du_an)
