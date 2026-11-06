# Thu nghiem cat chunk bang lon — v7.3.2 (chinh sach cat theo nhom dong)

Xem docstring cua `table_split.py` de biet chinh sach. So lieu do tren toan bo
1.313 file ingest-ready cua v7.3.1, khong sua du lieu goc.

| Chi so | Truoc | Sau |
|---|---|---|
| Tong chunk | 13,021 | 13,958 |
| Chunk bang [BANG] | 425 | 1362 |
| Chunk > 1.200 ky tu | 463 | 464 |
| Chunk > 5.000 ky tu | 67 | 2 |
| Chunk dai nhat (ky tu) | 65,302 | 6,174 |

- So bang bi cat: 210 (chi cat bang > 1.200 ky tu; bang nho giu nguyen).
- Kiem chung bat bien: 0 bang vi pham (dong du lieu + dong tra cuu phai
  khop dung thu tu sau khi cat, tru dong header lap lai).
- 21 bang co so dong [DANG TRA CUU] khac so dong du lieu trong
  ban goc — voi cac bang nay dong tra cuu duoc phan phoi theo ty le vi tri dong,
  khong dam bao gh ep cap 1-1 tung dong; can doi chieu rieng neu dung lam
  du lieu tra cuu chinh xac.
- Phan du sau cat: 211 chunk con cua bang van
  > 1.200 ky tu (trong do 87 chunk > 2.000 va
  2 chunk > 5.000). Hai nguyen nhan da xac minh
  bang doc mau that: (1) bang qua rong — rieng khoi header lap lai da ~900 ky
  tu (vd bang giang vien de an 2021, 11 cot) nen header + 1 dong + dong tra cuu
  tuong ung da vuot tran 1.200, khong cat nho hon duoc ma khong pha cau truc;
  (2) bang dang bieu mau (nhieu nhat o muc tuyen dung) — moi dong [DANG TRA CUU]
  la mot muc dai vai nghin ky tu chua toan bo noi dung bieu mau, cat theo dong
  khong chia nho duoc muc do. Phan du nay da duoc chot o muc 7 ban trinh bay v7.3.2: giu nguyen,
  khong cat tiep trong dong tra cuu, khong doi tran rieng cho chunk bang.
- Ngoai chunk bang, chunk van ban thuong vuot nhe (toi da ~1.280 ky tu) van
  con nhu ghi nhan o dry-run va khong doi sau thu nghiem nay.
