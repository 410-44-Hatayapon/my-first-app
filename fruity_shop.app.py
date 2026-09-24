import streamlit as st


# ============================================================
# ตั้งค่าหน้าเว็บ
# ============================================================
st.set_page_config(
    page_title="Fruity Shop",
    page_icon="🍉",
    layout="wide"
)


# ============================================================
# CSS ตกแต่ง
# ============================================================
st.markdown(
    """
    <style>
        .main {
            background-color: white;
        }

        .shop-title {
            font-size: 65px;
            font-weight: 900;
            margin-bottom: 20px;
        }

        .fruit-card {
            text-align: center;
            padding: 10px;
        }

        .fruit-name {
            font-size: 24px;
            font-weight: bold;
        }

        .fruit-price {
            font-size: 19px;
            font-weight: 600;
            margin-bottom: 8px;
        }

        .count-box {
            text-align: center;
            font-size: 22px;
            font-weight: bold;
            padding-top: 5px;
        }

        .info-box {
            border: 2px solid #555;
            padding: 18px;
            margin-top: 15px;
            margin-bottom: 15px;
            background-color: white;
        }

        .info-title {
            font-size: 25px;
            font-weight: bold;
        }

        .cart-item {
            font-size: 18px;
            margin-bottom: 8px;
        }

        .total-price {
            font-size: 30px;
            font-weight: bold;
        }
    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# ข้อมูลผลไม้
# ============================================================
fruits = {
    "Watermelon": {
        "price": 50,
        "emoji": "🍉"
    },
    "Kiwi": {
        "price": 35,
        "emoji": "🥝"
    },
    "Strawberry": {
        "price": 30,
        "emoji": "🍓"
    },
    "Mango": {
        "price": 30,
        "emoji": "🥭"
    },
    "Blueberry": {
        "price": 35,
        "emoji": "🫐"
    },
    "Apple": {
        "price": 20,
        "emoji": "🍎"
    }
}


# ============================================================
# สร้างตัวแปรจำนวนสินค้าใน Session State
# ============================================================
for fruit in fruits:
    if f"qty_{fruit}" not in st.session_state:
        st.session_state[f"qty_{fruit}"] = 0


# ============================================================
# ชื่อร้าน
# ============================================================
st.markdown(
    '<div class="shop-title">Fruity Shop 🍉</div>',
    unsafe_allow_html=True
)


# ============================================================
# แสดงผลไม้ 6 ชนิด
# ============================================================
columns = st.columns(3)

for index, (fruit, data) in enumerate(fruits.items()):

    with columns[index % 3]:

        st.markdown(
            '<div class="fruit-card">',
            unsafe_allow_html=True
        )

        # รูปผลไม้
        st.markdown(
            f"""
            <div style="
                font-size: 120px;
                text-align: center;
                height: 145px;
            ">
                {data["emoji"]}
            </div>
            """,
            unsafe_allow_html=True
        )

        # ชื่อผลไม้
        st.markdown(
            f'<div class="fruit-name">{fruit}</div>',
            unsafe_allow_html=True
        )

        # ราคา
        st.markdown(
            f'<div class="fruit-price">{data["price"]} baht/kg</div>',
            unsafe_allow_html=True
        )

        # ปุ่มลด / จำนวน / เพิ่ม
        c1, c2, c3 = st.columns([1, 1, 1])

        # ปุ่ม -
        with c1:
            if st.button(
                "-",
                key=f"minus_{fruit}",
                use_container_width=True
            ):
                if st.session_state[f"qty_{fruit}"] > 0:
                    st.session_state[f"qty_{fruit}"] -= 1
                    st.rerun()

        # แสดงจำนวน
        with c2:
            st.markdown(
                f"""
                <div class="count-box">
                    {st.session_state[f"qty_{fruit}"]}
                </div>
                """,
                unsafe_allow_html=True
            )

        # ปุ่ม +
        with c3:
            if st.button(
                "+",
                key=f"plus_{fruit}",
                use_container_width=True
            ):
                st.session_state[f"qty_{fruit}"] += 1
                st.rerun()

        st.markdown(
            '</div>',
            unsafe_allow_html=True
        )

    # เส้นแบ่งหลังผลไม้แถวที่ 3
    if index == 2:
        st.divider()


# ============================================================
# คำนวณราคาสินค้าในตะกร้า
# ============================================================
cart = []
subtotal = 0

for fruit, data in fruits.items():

    quantity = st.session_state[f"qty_{fruit}"]

    if quantity > 0:

        # ราคาปกติ
        normal_price = quantity * data["price"]

        # ====================================================
        # โปรโมชั่นผลไม้ราคา 35 บาท
        # ซื้อครบ 3 kg = 100 บาท
        # ====================================================
        if data["price"] == 35 and quantity >= 3:

            groups = quantity // 3
            remainder = quantity % 3

            product_price = (
                groups * 100
                + remainder * 35
            )

            promotion_text = "โปร 3 kg = 100 บาท"

        else:

            product_price = normal_price
            promotion_text = ""

        # เพิ่มสินค้าเข้าตะกร้า
        cart.append(
            {
                "name": fruit,
                "quantity": quantity,
                "price": product_price,
                "normal_price": normal_price,
                "promotion": promotion_text
            }
        )

        subtotal += product_price


# ============================================================
# คำนวณส่วนลด 5%
# ============================================================
if subtotal >= 150:

    discount = subtotal * 0.05
    discount_text = f"ส่วนลด 5% = {discount:.2f} บาท"

else:

    discount = 0
    discount_text = "ยังไม่ได้รับส่วนลด 5%"


# ============================================================
# ราคาหลังหักส่วนลด
# ============================================================
price_after_discount = subtotal - discount


# ============================================================
# VAT 7%
# ============================================================
vat = price_after_discount * 0.07

net_price = price_after_discount + vat


# ============================================================
# ส่วนล่างของเว็บไซต์
# ============================================================
left, right = st.columns([1.25, 1])


# ============================================================
# กล่องซ้าย : ส่วนลดของร้านค้า
# ============================================================
with left:

    st.markdown(
        """
        <div class="info-box">

            <div class="info-title">
                ส่วนลดของร้านค้า
            </div>

            <br>

            • เมื่อซื้อสินค้าครบ <b>150 บาท</b>
            จะได้รับส่วนลด <b>5%</b>

            <br><br>

            • เมื่อซื้อสินค้าราคา <b>35 บาท/kg</b>
            ครบ <b>3 kg</b>
            จากเดิม 105 บาท เหลือ <b>100 บาท</b>

        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# กล่องขวา : ตะกร้าสินค้า
# ============================================================
with right:

    st.markdown(
        """
        <div class="info-box">

            <div class="info-title">
                🛒 ตะกร้าสินค้า
            </div>

            <br>
        """,
        unsafe_allow_html=True
    )

    if len(cart) == 0:

        st.write("ยังไม่มีสินค้าในตะกร้า")

    else:

        for item in cart:

            promotion = ""

            if item["promotion"]:
                promotion = (
                    f'<br><small>🏷️ {item["promotion"]}</small>'
                )

            st.markdown(
                f"""
                <div class="cart-item">
                    {item["quantity"]} kg
                    &nbsp; {item["name"]}
                    &nbsp; {item["price"]:.2f} บาท
                    {promotion}
                </div>
                """,
                unsafe_allow_html=True
            )

    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )


# ============================================================
# แสดงผลส่วนลด / VAT / ราคาสุทธิ
# ============================================================
left2, right2 = st.columns([1.25, 1])


# ============================================================
# กล่องส่วนลด
# ============================================================
with right2:

    st.markdown(
        f"""
        <div class="info-box">

            <div class="info-title">
                ส่วนลด
            </div>

            <br>

            {discount_text}

            <br><br>

            ราคาหลังหักส่วนลด:
            <b>{price_after_discount:.2f} บาท</b>

        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# กล่อง VAT
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
# กล่องราคาสุทธิ
# ============================================================
with right2:

    st.markdown(
        f"""
        <div class="info-box">

            <div class="info-title">
                ราคาสุทธิ
            </div>

            <br>

            <div class="total-price">
                {net_price:.2f} บาท
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )
# ============================================================
# ปุ่มยืนยันการซื้อ
# ============================================================
st.divider()

st.markdown(
    """
    <div style="
        text-align: center;
        font-size: 28px;
        font-weight: bold;
        margin-bottom: 15px;
    ">
        🛒 ยืนยันการสั่งซื้อ
    </div>
    """,
    unsafe_allow_html=True
)

# ปุ่มยืนยันการซื้อ
if st.button(
    "✅ ยืนยันการซื้อ",
    use_container_width=True,
    type="primary"
):

    # ตรวจสอบว่ามีสินค้าในตะกร้าหรือไม่
    if len(cart) == 0:

        st.warning("⚠️ กรุณาเลือกสินค้าก่อนทำการซื้อ")

    else:

        st.success("🎉 ยืนยันการซื้อเรียบร้อยแล้ว!")

        st.markdown(
            """
            ### 🧾 รายละเอียดการสั่งซื้อ
            """,
        )

        # แสดงรายการสินค้า
        for item in cart:

            st.write(
                f"🍎 **{item['name']}** "
                f"{item['quantity']} kg "
                f"= {item['price']:.2f} บาท"
            )

        st.divider()

        # สรุปราคา
        st.write(f"**ราคาสินค้ารวม:** {subtotal:.2f} บาท")
        st.write(f"**ส่วนลด:** {discount:.2f} บาท")
        st.write(f"**VAT 7%:** {vat:.2f} บาท")

        st.markdown(
            f"""
            <div style="
                background-color: #e8f5e9;
                border: 2px solid #4caf50;
                border-radius: 10px;
                padding: 15px;
                text-align: center;
                margin-top: 15px;
            ">
                <div style="
                    font-size: 22px;
                    font-weight: bold;
                ">
                    💰 ราคาสุทธิ
                </div>

                <div style="
                    font-size: 35px;
                    font-weight: bold;
                    color: #2e7d32;
                ">
                    {net_price:.2f} บาท
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
# ============================================================
# สถานะการซื้อ
# ============================================================

if "purchase_completed" not in st.session_state:
    st.session_state.purchase_completed = False


# ============================================================
# ปุ่มยืนยันการซื้อ
# ============================================================

st.divider()

if not st.session_state.purchase_completed:

    st.markdown(
        """
        <div style="
            text-align: center;
            font-size: 28px;
            font-weight: bold;
            margin-bottom: 15px;
        ">
            🛒 พร้อมสั่งซื้อ
        </div>
        """,
        unsafe_allow_html=True
    )

    if st.button(
        "✅ ยืนยันการซื้อ",
        use_container_width=True,
        type="primary"
    ):

        if len(cart) == 0:

            st.warning(
                "⚠️ กรุณาเลือกสินค้าก่อนทำการซื้อ"
            )

        else:

            # เปลี่ยนสถานะเป็นซื้อเสร็จแล้ว
            st.session_state.purchase_completed = True

            st.rerun()


# ============================================================
# หน้าหลังจากซื้อเสร็จ
# ============================================================

else:

    st.success("🎉 ซื้อสินค้าเรียบร้อยแล้ว!")

    st.markdown(
        """
        <div style="
            background-color: #e8f5e9;
            border: 2px solid #4caf50;
            border-radius: 12px;
            padding: 20px;
            text-align: center;
            margin-top: 15px;
            margin-bottom: 20px;
        ">

            <div style="
                font-size: 30px;
                font-weight: bold;
                color: #2e7d32;
            ">
                🧾 การสั่งซื้อสำเร็จ
            </div>

            <br>

            <div style="font-size: 20px;">
                ขอบคุณที่ใช้บริการ Fruity Shop 🍉
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

    # ========================================================
    # สรุปรายการซื้อ
    # ========================================================

    st.markdown("### 🧾 รายการที่ซื้อ")

    for item in cart:

        st.write(
            f"🍎 **{item['name']}** "
            f"{item['quantity']} kg "
            f"= {item['price']:.2f} บาท"
        )

    st.divider()

    # ========================================================
    # สรุปราคา
    # ========================================================

    st.write(
        f"**ราคาสินค้า:** {subtotal:.2f} บาท"
    )

    st.write(
        f"**ส่วนลด:** -{discount:.2f} บาท"
    )

    st.write(
        f"**VAT 7%:** {vat:.2f} บาท"
    )

    st.markdown(
        f"""
        <div style="
            background-color: #fff8e1;
            border: 2px solid #ffb300;
            border-radius: 12px;
            padding: 20px;
            text-align: center;
            margin-top: 15px;
            margin-bottom: 20px;
        ">

            <div style="
                font-size: 22px;
                font-weight: bold;
            ">
                💰 ราคาสุทธิ
            </div>

            <div style="
                font-size: 38px;
                font-weight: bold;
                color: #e65100;
            ">
                {net_price:.2f} บาท
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

    # ========================================================
    # ตะกร้าถัดไป
    # ========================================================

    if st.button(
        "🛒 ซื้อตะกร้าถัดไป",
        use_container_width=True,
        type="primary"
    ):

        # ล้างจำนวนสินค้าทุกชนิด
        for fruit in fruits:
            st.session_state[f"qty_{fruit}"] = 0

        # กลับไปสถานะเลือกซื้อ
        st.session_state.purchase_completed = False

        # รีเฟรชหน้า
        st.rerun()
