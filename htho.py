import urllib.request
import json
import datetime
import os

url = "https://wtxmd52.tele68.com/v1/txmd5/sessions"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
res = urllib.request.urlopen(req)
json_data = json.loads(res.read().decode())
data = json_data.get('list', [])

if data:
    now = datetime.datetime.now()
    time_now = now.strftime("%Y-%m-%d %H:%M:%S")
    
    # TỰ ĐỘNG TÌM SỐ THỨ TỰ TIẾP THEO (1, 2, 3...)
    counter = 1
    while os.path.exists(f"{counter}.txt"):
        counter += 1
    filename = f"{counter}.txt"
    
    total = len(data)
    line = "=" * 50
    dash = "-" * 50
    
    p1 = [line, "DANH SACH KET QUA XUC XAC", f"Thoi gian: {time_now}", f"Tong so phien: {total}", line, "", f"{'STT':<5} {'ID':<12} {'KQ':<6} {'Xuc xac':<12} {'Diem':<6}", dash]

    for i, item in enumerate(data, start=1):
        xx = item.get('dices', [0,0,0])
        xx_str = f"[{xx[0]},{xx[1]},{xx[2]}]"
        kq = item.get('resultTruyenThong', 'N/A')
        id_str = str(item.get('id', ''))
        point = str(item.get('point', 0))
        p1.append(f"{i:<5} {id_str:<12} {kq:<6} {xx_str:<12} {point:<6}")

    p2 = ["", line, "THONG KE TONG HOP", dash]
    tai = sum(1 for item in data if item.get('resultTruyenThong') == "TAI")
    xiu = total - tai
    tai_pct = round((tai / total) * 100) if total > 0 else 0
    xiu_pct = round((xiu / total) * 100) if total > 0 else 0
    p2.append(f"Tong so phien: {total}")
    p2.append(f"TAI: {tai} ({tai_pct}%)")
    p2.append(f"XIU: {xiu} ({xiu_pct}%)")
    
    points = [item.get('point', 0) for item in data]
    p2.append("Thong ke diem so:")
    p2.append(f"  - Cao nhat: {max(points)}")
    p2.append(f"  - Thap nhat: {min(points)}")
    p2.append(f"  - Trung binh: {round(sum(points) / total, 2)}")
    
    p2.append("Phan phoi diem:")
    counts = {}
    for d in points:
        counts[d] = counts.get(d, 0) + 1
    for pt in sorted(counts.keys()):
        p2.append(f"  - Diem {pt}: {counts[pt]} lan")

    p2.append("")
    p2.append(line)
    p2.append(f"[OK] ID dau tien: {data[0].get('id', '')}")
    p2.append(f"[OK] ID cuoi cung: {data[-1].get('id', '')}")
    
    report = "\n".join(p1) + "\n" + "\n".join(p2)
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write(report)
    print(f"=> Thanh cong! Da tao file: {filename}")
else:
    print("Loi: Khong lay duoc du lieu.")