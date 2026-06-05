"""
MNIST 画板预处理 — 与 Keras MNIST 训练格式一致

Streamlit 画板：白字黑底 float 0~1
Keras MNIST：  白字黑底（笔画亮、背景暗）

流程：×255 → 灰度 → 裁剪居中 → 缩放到 28×28 → /255
"""

import cv2
import numpy as np

MNIST_SIZE = 28
DIGIT_SIZE = 20
CANVAS_SIZE = 150


def _ensure_uint8(image: np.ndarray) -> np.ndarray:
    img = np.asarray(image)
    if img.dtype in (np.float32, np.float64) or (img.size > 0 and img.max() <= 1.0):
        img = (img * 255).clip(0, 255)
    return img.astype(np.uint8)


def _to_grey(image: np.ndarray) -> np.ndarray:
    img = _ensure_uint8(image)
    if img.ndim == 3:
        if img.shape[2] == 4:
            return cv2.cvtColor(img, cv2.COLOR_RGBA2GRAY)
        return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return img


def center_digit(grey_uint8: np.ndarray) -> np.ndarray:
    """白字黑底灰度图 → 居中缩放到 28×28（与 MNIST 一致，不反色）。"""
    _, binary = cv2.threshold(grey_uint8, 30, 255, cv2.THRESH_BINARY)
    coords = cv2.findNonZero(binary)
    if coords is None:
        return np.zeros((MNIST_SIZE, MNIST_SIZE), dtype=np.uint8)

    x, y, w, h = cv2.boundingRect(coords)
    digit = grey_uint8[y : y + h, x : x + w]

    scale = DIGIT_SIZE / max(w, h)
    nw = max(1, int(w * scale))
    nh = max(1, int(h * scale))
    resized = cv2.resize(digit, (nw, nh), interpolation=cv2.INTER_AREA)

    canvas = np.zeros((MNIST_SIZE, MNIST_SIZE), dtype=np.uint8)
    ox = (MNIST_SIZE - nw) // 2
    oy = (MNIST_SIZE - nh) // 2
    canvas[oy : oy + nh, ox : ox + nw] = resized
    return canvas


def normalize(mnist_uint8: np.ndarray) -> np.ndarray:
    return (mnist_uint8.astype(np.float32) / 255.0).reshape(1, MNIST_SIZE, MNIST_SIZE, 1)


def preprocess_canvas(image: np.ndarray) -> np.ndarray:
    grey = _to_grey(image)
    return normalize(center_digit(grey))


def preprocess_png_bytes(contents: bytes) -> np.ndarray:
    nparr = np.frombuffer(contents, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    if img is None:
        raise ValueError("无法解码 PNG")
    grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return normalize(center_digit(grey))


def canvas_to_png_bytes(image: np.ndarray) -> bytes:
    img = _ensure_uint8(image)
    if img.ndim == 3 and img.shape[2] == 4:
        img = cv2.cvtColor(img, cv2.COLOR_RGBA2BGR)
    ok, buf = cv2.imencode(".png", img)
    if not ok:
        raise ValueError("PNG 编码失败")
    return buf.tobytes()


def preprocess_for_display(image: np.ndarray, size: int = 192) -> np.ndarray:
    batch = preprocess_canvas(image)
    preview = (batch[0, :, :, 0] * 255).astype(np.uint8)
    return cv2.resize(preview, (size, size), interpolation=cv2.INTER_NEAREST)


def batch_for_model(batch: np.ndarray, model) -> np.ndarray:
    if model.input_shape is not None and len(model.input_shape) == 3:
        return batch.reshape(batch.shape[0], MNIST_SIZE, MNIST_SIZE)
    return batch


def render_on_canvas(mnist_digit_u8: np.ndarray) -> np.ndarray:
    """MNIST 单张图（28×28 白字黑底 uint8）→ 150×150 画板 RGBA float32。"""
    stroke = mnist_digit_u8.copy()
    stroke = cv2.dilate(stroke, np.ones((2, 2), np.uint8), iterations=1)

    scale = np.random.uniform(1.8, 3.0)
    new_size = max(20, min(80, int(28 * scale)))
    stroke_big = cv2.resize(stroke, (new_size, new_size), interpolation=cv2.INTER_AREA)

    canvas = np.zeros((CANVAS_SIZE, CANVAS_SIZE), dtype=np.uint8)
    ox = np.random.randint(5, max(6, CANVAS_SIZE - new_size - 5))
    oy = np.random.randint(5, max(6, CANVAS_SIZE - new_size - 5))
    canvas[oy : oy + new_size, ox : ox + new_size] = np.maximum(
        canvas[oy : oy + new_size, ox : ox + new_size], stroke_big
    )

    rgba = np.zeros((CANVAS_SIZE, CANVAS_SIZE, 4), dtype=np.float32)
    rgba[:, :, :3] = canvas[:, :, None] / 255.0
    rgba[:, :, 3] = 1.0
    mask = canvas > 0
    rgba[mask, 0] = 1.0
    rgba[mask, 1] = 1.0
    rgba[mask, 2] = 1.0
    return rgba


def mnist_to_model_input(mnist_img: np.ndarray) -> np.ndarray:
    """MNIST float (28,28,1) → 模拟画板 → preprocess，用于训练。"""
    if mnist_img.max() <= 1.0:
        u8 = (mnist_img.squeeze() * 255).astype(np.uint8)
    else:
        u8 = mnist_img.squeeze().astype(np.uint8)
    canvas = render_on_canvas(u8)
    return preprocess_canvas(canvas)
