import streamlit as st

# =========================
# ตั้งค่าหน้าเว็บ
# =========================
st.set_page_config(
page_title="Fruity Shop",
page_icon="🍉",
layout="wide")

# =========================
# CSS ตกแต่ง
# =========================
st.markdown("""
<style>

.main {background-color: white;}

.shop-title {font-size: 65px;font-weight: 900;margin-bottom: 20px;}

.fruit-card {text-align: center;padding: 10px;}

.fruit-name {font-size: 24px;font-weight: bold;}

.fruit-price {font-size: 19px;font-weight: 600;margin-bottom: 8px;}

.count-box {text-align: center;font-size: 22px;font-weight: bold;padding-top: 5px;}

.info-box {border: 2px solid #555;padding: 18px;margin-top: 15px;margin-bottom: 15px;background-color: white;}

.info-title {font-size: 25px;font-weight: bold;}

.cart-item {font-size: 18px;margin-bottom: 8px;}

.total-price {font-size: 30px;font-weight: bold;}

</style>
""", unsafe_allow_html=True)


# =========================
# ข้อมูลผลไม้
# =========================
fruits = {
"Watermelon": {"price": 50,"emoji": "🍉"},
"Kiwi": {"price": 35,"emoji": "🥝"},
"Strawberry": {"price": 30,"emoji": "🍓"},
"Mango": {"price": 30,"emoji": "🥭"},
"Blueberry": {"price": 35,"emoji": "🫐"},
"Apple": {"price": 20,"emoji": "🍎"}}


# =========================
# สร้างตัวแปรจำนวนสินค้า
# สร้างตัวแปรจำนวนสินค้า
 for fruit in fruits:
     if f"qty_{fruit}" not in st.session_state:
        st.session_state[f"qty_{fruit}"] = 0

# =========================
# ชื่อร้าน
# =========================
st.markdown('<div class="shop-title">Fruity Shop</div>',unsafe_allow_html=True)


# =========================
# แสดงผลไม้ 6 ชนิด
# =========================
columns = st.columns(3)

for index, (fruit, data) in enumerate(fruits.items()):

with columns[index % 3]:

st.markdown('<div class="fruit-card">',unsafe_allow_html=True)

# รูปผลไม้
st.markdown(f"""<div style="font-size:120px;text-align:center;height:145px;">
{data["emoji"]}</div>""",unsafe_allow_html=True)

# ชื่อ
st.markdown(f'<div class="fruit-name">{fruit}</div>',unsafe_allow_html=True)

# ราคา
st.markdown(f'<div class="fruit-price">{data["price"]} baht/kg</div>',unsafe_allow_html=True)

# ปุ่ม - จำนวน +
c1, c2, c3 = st.columns([1, 1, 1])

with c1:
 # ปุ่ม - จำนวน +
c1, c2, c3 = st.columns([1, 1, 1])

with c1:
if st.button("-", key=f"minus_{fruit}", use_container_width=True):
if st.session_state[f"qty_{fruit}"] > 0:
st.session_state[f"qty_{fruit}"] -= 1
st.rerun()

with c2:
st.markdown(
f'<div class="count-box">{st.session_state[f"qty_{fruit}"]}</div>',
unsafe_allow_html=True
)

with c3:
if st.button("+", key=f"plus_{fruit}", use_container_width=True):
st.session_state[f"qty_{fruit}"] += 1
st.rerun()

st.markdown('</div>', unsafe_allow_html=True)


st.divider()


# ============================================================
# คำนวณราคาสินค้า
# ============================================================

cart = []
subtotal = 0

     for fruit, data in fruits.items():

quantity = st.session_state[f"qty_{fruit}"]

     if quantity > 0:

normal_price = quantity * data["price"]

# โปรผลไม้ราคา 35 บาท
# ครบ 3 kg = 100 บาท
     if data["price"] == 35 and quantity >= 3:

groups = quantity // 3
remainder = quantity % 3

product_price = (groups * 100+ remainder * 35)
promotion_text = "โปร 3 kg = 100 บาท"

     else:product_price = normal_price
promotion_text = ""

cart.append({"name": fruit,"quantity": quantity,"price": product_price,"normal_price": normal_price,"promotion": promotion_text})

subtotal += product_price


# ============================================================
# ส่วนล่าง
# ============================================================

left, right = st.columns([1.25, 1])


# ============================================================
# กล่องซ้าย : ส่วนลดของร้านค้า
# ============================================================

with left:

st.markdown("""<div class="info-box">
<div class="info-title">ส่วนลดของร้านค้า
</div>

<br>

• เมื่อซื้อสินค้าครบ <b>150 บาท</b>
จะได้รับส่วนลด <b>5%</b>

<br><br>

• เมื่อซื้อสินค้าราคา <b>35 บาท/kg</b>ครบ <b>3 kg</b>จากเดิม 105 บาท เหลือ <b>100 บาท</b></div>""",unsafe_allow_html=True)

# ============================================================
# กล่องขวา : ตะกร้าสินค้า
# ============================================================

with right:

st.markdown("""<div class="info-box">
<div class="info-title">ตะกร้าสินค้า
</div>
""",unsafe_allow_html=True)

    if len(cart) == 0:

st.write("ยังไม่มีสินค้าในตะกร้า")

else:

     for item in cart:

st.markdown(
f"""<div class="cart-item">{item["quantity"]} &nbsp;{item["name"]} &nbsp;{item["price"]} บาท</div>""",unsafe_allow_html=True)st.markdown("</div>", unsafe_allow_html=True)


# ============================================================
# คำนวณส่วนลด
# ============================================================

if subtotal >= 150:
discount = subtotal * 0.05
discount_text = f"ส่วนลด 5% = {discount:.2f} บาท"
else:
discount = 0
discount_text = "ยังไม่ได้รับส่วนลด 5%"


price_after_discount = subtotal - discount


# ============================================================
# VAT 7%
# ============================================================

vat = price_after_discount * 0.07

net_price = price_after_discount + vat


# ============================================================
# กล่องแสดงส่วนลด
# ============================================================

left2, right2 = st.columns([1.25, 1])

with right2:

st.markdown(f"""<div class="info-box">
<div class="info-title">

ส่วนลด
</div>

<br>

{discount_text}

<br><br>

ราคาหลังหักส่วนลด:
<b>{price_after_discount:.2f} บาท</b>
</div>""",unsafe_allow_html=True)


# ============================================================
# VAT
# ============================================================

with right2:

st.markdown(
f"""
<div class="info-box">
<div class="info-title">

VAT 7%
</div>

<br>

VAT = {vat:.2f} บาท

</div>
""",
unsafe_allow_html=True
)


# ============================================================
# ราคาสุทธิ
# ============================================================

with right2:

st.markdown(f"""<div class="info-box">

<div class="info-title">

ราคาสุทธิ
</div>

<br>

<div class="total-price">
{net_price:.2f} บาท
</div>

</div>
""",unsafe_allow_html=True)
