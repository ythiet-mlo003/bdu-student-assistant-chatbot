# Kiem toan bang v7.3 — sua lech dem 21 bang + loi cat bang So tay (13/10/2026)

Lam ro 2 diem treo ghi trong `pipeline-prep-v7.3/table-split-stats.md`:
(1) "21 bang co so dong tra cuu khac so dong du lieu" va (2) 211 chunk con
cua bang van >1.200 ky tu. Khong sua data v7.3, khong sua script goc.

## 1. Dem lai toan corpus: con so 21 vua thieu vua thua

Quet ca 424 bang cua 1.312 file ingest-ready (con so 21 cu chi dem cac
bang DUOC CAT, tuc bang >1.200 ky tu):

- Dem theo muc tra cuu (dong bat dau "- "): 36 bang bi gan co lech.
- Trong do **22 bang la bang So tay sinh vien** (daotao/so-tay-sinh-vien/)
  dung dinh dang tra cuu DONG THUAN — moi dong la 1 muc, khong co "- ".
  Doi chieu theo DONG: ca corpus co 23 bang dong thuan va **ca 23 bang
  deu du dung so dong = so dong du lieu**. Khong mat dong nao; day la
  khac dinh dang, khong phai thieu du lieu.
- **Lech that: 14 bang**, tat ca o dinh dang "- ", va tat ca deu thieu
  dong tra cuu (delta am). Phan bo: 9 bang la bieu mau tuyen dung
  can bo/giang vien 2023 (3 file, moi file 3 bang giong nhau — mau don
  ung tuyen), 2 bang tin tuyen dung doanh nghiep o muc groups, 1 bang
  bieu mau khoa hoc 2025, va **1 bang dang chu y**: bang 5 cua De an
  tuyen sinh dai hoc 2021 (bdu/thong-bao/2021) — 22 dong du lieu chi co
  15 dong tra cuu vi bang co header 2 tang (chi tieu / TS nhap hoc /
  diem trung tuyen theo 2 nam). Bang nay thuoc nhom diem/chitieu —
  khi chatbot tra cuu bang nay phai dua vao dong markdown goc, khong
  chi dua vao [DANG TRA CUU].

## 2. Loi that trong table_split.py voi bang So tay — da co ban va

Vi bo cat chi nhan muc tra cuu bat dau "- ", moi dong thuan bi gom thanh
1 muc khong lo, va ham phan phoi theo ty le day toan bo dong tra cuu vao
1 chunk con duy nhat. Do truc tiep tren bang Phan IV So tay (2.252 ky tu):
3 chunk con co so dong tra cuu la **0 / 14 / 0** — 2/3 chunk con mat han
phan [DANG TRA CUU], chunk con con lai phinh > tran vi chua ca 14 dong.

- Tong cong **12 bang dong thuan bi cat, ca 12/12 deu lech** kieu nay.
- Ban va `table_split_v2.py` (thu muc nay): nhan dien dinh dang dong
  thuan (khong dong nao bat dau "- ") thi coi moi dong la 1 muc.
  Ket qua do lai toan corpus:
  - Phan phoi lech: **12 -> 0**
  - Bat bien bao toan dong du lieu + dong tra cuu dung thu tu: **0 vi pham**
  - Chunk con cua bang lon >1.200 ky tu: **212 -> 206**; >5.000: giu 2;
    chunk dai nhat giu 6.174 ky tu
- Khi code pipeline that (giai doan 3/4), dung logic v2 nay thay cho
  table_split.py goc; script goc giu nguyen de doi chieu.

## 3. Phan du 211 chunk con >1.200 ky tu — phan bo de chot chinh sach

(table-split-stats dem 211 o cac bang duoc cat; audit nay dem 212 khi
tinh ca bang cat khong tach duoc — chenh 1 do cach dem, khong phai lech du lieu.)

- Theo nguyen nhan: 97 chunk do 1 dong tra cuu don le qua dai (>900 ky tu,
  chu yeu la bieu mau), chi 4 chunk do header bang qua rong, con lai la
  tong hop header + dong dai.
- Theo muc: groups 46, thong-tin-xet-tot-nghiep (tuyensinh) 42,
  thong-bao 22, tuyen dung giang vien 20, ke-hoach-thang 15,
  trang-chu 15, tuyen dung 13, gdqp-an 12, tuyen dung can bo 8...
  Rieng nhom tuyen dung + groups chiem ~87/212.
- Theo nam: 2023: 61, 2024: 43, 2026: 42, 2021: 31, 2025: 29.

He qua cho quyet dinh con treo: neu ap tran token cua model embedding
512 token thi nhom nay van bi cut; voi model 8.192 token (bge-m3) thi
206 chunk con lai deu nam trong gioi han (dai nhat 6.174 ky tu) — tuc
phan du nay chi la van de neu chon model token ngan, khong can cat
them trong dong tra cuu o vong nay.

## Tep trong thu muc
- `audit_tables.py` + `audit-results.json`: kiem toan lech dong + phan du
- `table_split_v2.py`: bo cat da va, da kiem chung bat bien toan corpus
