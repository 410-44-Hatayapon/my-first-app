# ============================================================
# สถานะการซื้อ
# ============================================================

if "purchase_completed" not in st.session_state:
    st.session_state.purchase_completed = False


# ============================================================
# ก่อนซื้อ
# ============================================================

if not st.session_state.purchase_completed:

    st.divider()

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

    # ใช้ key เพื่อป้องกันปุ่มซ้ำ
    if st.button(
        "✅ ยืนยันการซื้อ",
        key="confirm_purchase",
        use_container_width=True,
        type="primary"
    ):

        if len(cart) == 0:

            st.warning("⚠️ กรุณาเลือกสินค้าก่อนทำการซื้อ")

        else:

            st.session_state.purchase_completed = True

            st.rerun()


# ============================================================
# หลังซื้อเสร็จ
# ============================================================

else:

    st.divider()

    st.success("🎉 ซื้อสินค้าเรียบร้อยแล้ว!")

    st.markdown(
        """
        <div style="
            background-color: #e8f5e9;
            border: 2px solid #4caf50;
            border-radius: 12px;
            padding: 20px;
            text-align: center;
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
    # รายการสินค้าที่ซื้อ
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


    # ========================================================
    # ราคาสุทธิ
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
    # ซื้อตะกร้าถัดไป
    # ========================================================

    if st.button(
        "🛒 ซื้อตะกร้าถัดไป",
        key="next_cart",
        use_container_width=True,
        type="primary"
    ):

        # ล้างจำนวนสินค้าทั้งหมด
        for fruit in fruits:
            st.session_state[f"qty_{fruit}"] = 0

        # กลับไปหน้าซื้อสินค้า
        st.session_state.purchase_completed = False

        # รีเฟรช
        st.rerun()
