import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Lottery Noise App", layout="wide")

st.title("🎰 Lottery Noise Dashboard")
st.write("输入开奖（16位，例如：0413203137435109）")

# ===== 输入 =====
input_str = st.text_input("开奖字符串", "0413203137435109")

# ===== 校验 =====
if len(input_str) != 16 or not input_str.isdigit():
    st.warning("请输入16位数字")
    st.stop()

# ===== 编码函数 =====
def string_to_bits(s):
    return ''.join(format(ord(c), '08b') for c in s)

bits = string_to_bits(input_str)

# ===== 转信号 =====
signal = np.array([1 if b == '1' else -1 for b in bits])

# ===== 波形 =====
st.subheader("📈 波形图")
fig1, ax1 = plt.subplots()
ax1.plot(signal)
ax1.set_title("Time Domain Signal")
st.pyplot(fig1)

# ===== 频谱 =====
st.subheader("📊 频谱图")
fft = np.fft.fft(signal)
mag = np.abs(fft)

fig2, ax2 = plt.subplots()
ax2.plot(mag)
ax2.set_title("Frequency Spectrum")
st.pyplot(fig2)

# ===== 热力图 =====
st.subheader("🧩 热力图")
matrix = signal.reshape(8, 16)

fig3, ax3 = plt.subplots()
ax3.imshow(matrix, cmap='gray')
ax3.set_title("Bit Heatmap")
st.pyplot(fig3)

# ===== 熵 =====
st.subheader("🔥 熵值")

p = np.mean([1 if b == '1' else 0 for b in bits])

if p in [0, 1]:
    entropy = 0
else:
    entropy = -p*np.log2(p) - (1-p)*np.log2(1-p)

st.metric("Entropy", f"{entropy:.4f}")

# ===== 自动选号引擎 =====
st.subheader("🎲 自动选号")

def generate_numbers(bit_string):
    nums = []
    for i in range(0, len(bit_string), 6):
        chunk = bit_string[i:i+6]
        if len(chunk) < 6:
            break
        
        num = (int(chunk, 2) % 52) + 1
        
        if num not in nums:
            nums.append(num)
        
        if len(nums) == 8:
            break
    
    if len(nums) < 8:
        return None
    
    main = sorted(nums[:7])
    bonus = nums[7]
    
    return main, bonus

if st.button("生成号码"):
    result = generate_numbers(bits)
    
    if result:
        main, bonus = result
        st.success(f"主号: {main}")
        st.info(f"Bonus: {bonus}")
    else:
        st.error("生成失败")
