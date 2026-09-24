import streamlit as st


# ============================================================
# 1. ตั้งค่าหน้าเว็บ
# ============================================================

st.set_page_config(
    page_title="Fruity Shop",
    page_icon="🍉",
    layout="wide"
)


# ============================================================
# 2. CSS ตกแต่งเว็บไซต์
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
        border-radius: 10px;
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
        color: #e65100;
    }

    .success-box {
        background-color: #e8f5e9;
        border: 2px solid #4caf50;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        margin-top: 15px;
        margin-bottom: 20px;
    }

    .success-title {
        font-size: 30px;
        font-weight: bold;
        color: #2e7d32;
    }

    .success-text {
        font-size: 20px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# 3. ข้อมูลผลไม้
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
# 4. สร้าง Session State
# ============================================================

# จำนวนผลไม้แต่ละชนิด
for fruit in fruits:

    if f"qty_{fruit}" not in st.session_state:

        st.session_state[f"qty_{fruit}"] = 0


# สถานะการซื้อ
if "purchase_completed" not in st.session_state:

    st.session_state.purchase_completed = False


# ============================================================
# 5. ชื่อร้าน
# ============================================================

st.markdown(
    '<div class="shop-title">Fruity Shop 🍉</div>',
    unsafe_allow_html=True
)


# ============================================================
# 6. แสดงผลไม้
# ============================================================

columns = st.columns(3)


for index, (fruit, data) in enumerate(fruits.items()):

    with columns[index % 3]:

        st.markdown(
            '<div class="fruit-card">',
            unsafe_allow_html=True
        )

        # ----------------------------------------------------
        # รูปผลไม้
        # ----------------------------------------------------

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

        # ----------------------------------------------------
        # ชื่อผลไม้
        # ----------------------------------------------------

        st.markdown(
            f"""
            <div class="fruit-name">
                {fruit}
            </div>
            """,
            unsafe_allow_html=True
        )

        # ----------------------------------------------------
        # ราคา
        # ----------------------------------------------------

        st.markdown(
            f"""
            <div class="fruit-price">
                {data["price"]} baht/kg
            </div>
            """,
            unsafe_allow_html=True
        )

        # ----------------------------------------------------
        # ปุ่ม - จำนวน +
        # ----------------------------------------------------

        c1, c2, c3 = st.columns(3)

        # ปุ่มลดจำนวน
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

        # ปุ่มเพิ่มจำนวน
        with c3:

            if st.button(
                "+",
                key=f"plus_{fruit}",
                use_container_width=True
            ):

                st.session_state[f"qty_{fruit}"] += 1

                st.rerun()

        st.markdown(
            "</div>",
            unsafe_allow_html=True
        )


# ============================================================
# 7. คำนวณตะกร้าสินค้า
# ============================================================

cart = []

subtotal = 0


for fruit, data in fruits.items():

    quantity = st.session_state[f"qty_{fruit}"]

    # --------------------------------------------------------
    # ถ้ามีสินค้า
    # --------------------------------------------------------

    if quantity > 0:

        # ราคาปกติ
        normal_price = quantity * data["price"]

        # ----------------------------------------------------
        # โปรโมชั่น
        #
        # ผลไม้ราคา 35 บาท
        # ซื้อ 3 kg = 100 บาท
        # ----------------------------------------------------

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

        # ----------------------------------------------------
        # เพิ่มสินค้าเข้าตะกร้า
        # ----------------------------------------------------

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
# 8. คำนวณส่วนลด
# ============================================================

if subtotal >= 150:

    discount = subtotal * 0.05

    discount_text = (
        f"ส่วนลด 5% = {discount:.2f} บาท"
    )

else:

    discount = 0

    discount_text = "ยังไม่ได้รับส่วนลด 5%"


# ============================================================
# 9. คำนวณราคาหลังหักส่วนลด
# ============================================================

price_after_discount = subtotal - discount


# ============================================================
# 10. คำนวณ VAT 7%
# ============================================================

vat = price_after_discount * 0.07


# ============================================================
# 11. ราคาสุทธิ
# ============================================================

net_price = price_after_discount + vat


# ============================================================
# 12. ส่วนแสดงข้อมูลร้านค้าและตะกร้า
# ============================================================

left, right = st.columns([1.25, 1])


# ============================================================
# 13. กล่องโปรโมชั่นร้านค้า
# ============================================================

with left:

    st.markdown(
        """
        <div class="info-box">

            <div class="info-title">
                🎁 ส่วนลดของร้านค้า
            </div>

            <br>

            • เมื่อซื้อสินค้าครบ
            <b>150 บาท</b>
            จะได้รับส่วนลด
            <b>5%</b>

            <br><br>

            • ผลไม้ราคา
            <b>35 บาท/kg</b>
            ซื้อครบ
            <b>3 kg</b>

            <br>

            จากเดิม 105 บาท
            เหลือ
            <b>100 บาท</b>

        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# 14. ตะกร้าสินค้า
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

    # --------------------------------------------------------
    # ไม่มีสินค้า
    # --------------------------------------------------------

    if len(cart) == 0:

        st.write("ยังไม่มีสินค้าในตะกร้า")

    # --------------------------------------------------------
    # มีสินค้า
    # --------------------------------------------------------

    else:

        for item in cart:

            st.markdown(
                f"""
                <div class="cart-item">

                    {item["quantity"]} kg
                    &nbsp;
                    <b>{item["name"]}</b>
                    &nbsp;
                    {item["price"]:.2f} บาท

                </div>
                """,
                unsafe_allow_html=True
            )

            # แสดงโปรโมชั่น
            if item["promotion"]:

                st.caption(
                    f"🏷️ {item['promotion']}"
                )

    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )


# ============================================================
# 15. กล่องส่วนลด
# ============================================================

left2, right2 = st.columns([1.25, 1])


with right2:

    st.markdown(
        f"""
        <div class="info-box">

            <div class="info-title">
                💸 ส่วนลด
            </div>

            <br>

            {discount_text}

            <br><br>

            ราคาหลังหักส่วนลด:

            <b>
                {price_after_discount:.2f} บาท
            </b>

        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# 16. กล่อง VAT
# ============================================================

with right2:

    st.markdown(
        f"""
        <div class="info-box">

            <div class="info-title">
                VAT 7%
            </div>

            <br>

            VAT =
            <b>{vat:.2f} บาท</b>

        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# 17. กล่องราคาสุทธิ
# ============================================================

with right2:

    st.markdown(
        f"""
        <div class="info-box">

            <div class="info-title">
                💰 ราคาสุทธิ
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
# 18. ยืนยันการซื้อ
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

    # --------------------------------------------------------
    # ปุ่มยืนยันการซื้อ
    #
    # มี key เฉพาะ ป้องกัน DuplicateElementId
    # --------------------------------------------------------

    if st.button(
        "✅ ยืนยันการซื้อ",
        key="confirm_purchase",
        use_container_width=True,
        type="primary"
    ):

        # ตรวจสอบว่ามีสินค้า
        if len(cart) == 0:

            st.warning(
                "⚠️ กรุณาเลือกสินค้าก่อนทำการซื้อ"
            )

        else:

            # เปลี่ยนสถานะเป็นซื้อเสร็จ
            st.session_state.purchase_completed = True

            st.rerun()


# ============================================================
# 19. หลังจากซื้อเสร็จ
# ============================================================

else:

    st.markdown(
        """
        <div class="success-box">

            <div class="success-title">
                🎉 ซื้อสินค้าเรียบร้อยแล้ว!
            </div>

            <br>

            <div class="success-text">
                ขอบคุณที่ใช้บริการ Fruity Shop 🍉
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


    # ========================================================
    # 20. ใบสรุปรายการซื้อ
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
    # 21. สรุปราคา
    # ========================================================

    st.write(
        f"**ราคาสินค้ารวม:** "
        f"{subtotal:.2f} บาท"
    )

    st.write(
        f"**ส่วนลด:** "
        f"-{discount:.2f} บาท"
    )

    st.write(
        f"**VAT 7%:** "
        f"{vat:.2f} บาท"
    )


    # ========================================================
    # 22. แสดงราคาสุทธิหลังซื้อ
    # ========================================================

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
    # 23. ปุ่มซื้อตะกร้าถัดไป
    # ========================================================

    if st.button(
        "🛒 ซื้อตะกร้าถัดไป",
        key="next_cart",
        use_container_width=True,
        type="primary"
    ):

        # ----------------------------------------------------
        # ล้างจำนวนสินค้าทั้งหมด
        # ----------------------------------------------------

        for fruit in fruits:

            st.session_state[f"qty_{fruit}"] = 0


        # ----------------------------------------------------
        # กลับสู่สถานะพร้อมซื้อ
        # ----------------------------------------------------

        st.session_state.purchase_completed = False


        # ----------------------------------------------------
        # รีเฟรชหน้า
        # ----------------------------------------------------

        st.rerun()
