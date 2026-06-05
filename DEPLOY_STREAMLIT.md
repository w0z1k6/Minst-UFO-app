# 部署到 Streamlit Cloud（与同学同款 *.streamlit.app 链接）

同学的应用托管在 **Streamlit Community Cloud**（免费），地址形如：

- `https://app-homework-xxxxx.streamlit.app/`

你需要：**把代码推到 GitHub → 在 Streamlit 网站连接仓库 → 各部署一个 App**。

---

## 一、准备清单

| 应用 | 入口文件 | 依赖文件 | 模型文件（必须进仓库） |
|------|----------|----------|------------------------|
| **MNIST** | `machine_learning_web_app/app.py` | `machine_learning_web_app/environment.yml`（固定 Python 3.11） | `machine_learning_web_app/mnist.hdf5`（约 1.6MB） |
| **UFO** | `ufo_project/app.py` | `ufo_project/requirements.txt` | `ufo_project/ufo-model.pkl` |

本地已提供 **单体版** `app.py`（不依赖 FastAPI），适合云端一键运行。

---

## 二、上传到 GitHub

### 1. 注册 / 登录 GitHub

https://github.com

### 2. 新建空仓库

本仓库：**https://github.com/w0z1k6/Minst-UFO-app**

### 3. 在本机推送代码

在 PowerShell 中（路径按你的实际目录修改）：

```powershell
cd "E:\SHU sem.8\机器学习\Week5_Practice"

git init
git add .gitignore
git add machine_learning_web_app/app.py machine_learning_web_app/preprocess.py machine_learning_web_app/environment.yml machine_learning_web_app/.python-version machine_learning_web_app/mnist.hdf5
git add ufo_project/app.py ufo_project/requirements.txt ufo_project/ufo-model.pkl
git add DEPLOY_STREAMLIT.md

git commit -m "Week5 MNIST and UFO Streamlit apps for cloud deploy"

git branch -M main
git remote add origin https://github.com/w0z1k6/Minst-UFO-app.git
git push -u origin main
```

> **注意**：`mnist.hdf5` 必须提交，否则云端无法加载模型。  
> 不要上传 `venv/`、`.venv/`（已在 `.gitignore` 中）。

若 GitHub 要求登录，可用 **Personal Access Token** 作为密码，或安装 [GitHub Desktop](https://desktop.github.com/) 图形化推送。

---

## 三、在 Streamlit Cloud 创建应用

1. 打开 **https://share.streamlit.io** ，用 GitHub 账号登录  
2. 点击 **Create app** → **From existing repo**  
3. 选择你的仓库 `w0z1k6/Minst-UFO-app`、分支 `main`

### 部署 MNIST（第一个 App）

| 设置项 | 填写内容 |
|--------|----------|
| **Main file path** | `machine_learning_web_app/app.py` |
| **App URL**（可选） | 例如 `week5-mnist-你的名字` |

点击 **Deploy**。首次会安装 `tensorflow-cpu`，约 **5–15 分钟**，属正常情况。

### 部署 UFO（第二个 App）

再次 **Create app**，同一仓库，不同入口：

| 设置项 | 填写内容 |
|--------|----------|
| **Main file path** | `ufo_project/app.py` |
| **App URL** | 例如 `week5-ufo-你的名字` |

UFO 依赖少，一般 **1–3 分钟** 即可上线。

---

## 四、提交作业时写什么

在报告或作业里附上两个链接，例如：

```
MNIST Digit Recognizer: https://week5-mnist-xxx.streamlit.app/
UFO Sighting Predictor:  https://week5-ufo-xxx.streamlit.app/
```

（以 Streamlit 实际生成的域名为准。）

---

## 五、常见问题

### 1. 部署失败：找不到 `mnist.hdf5`

确认已 `git add machine_learning_web_app/mnist.hdf5` 并 push。

### 2. `Error installing requirements` / `tensorflow-cpu` / Python 3.14

Streamlit 若使用 **Python 3.14**，TensorFlow 无法安装。本仓库已用 `environment.yml` 固定 **Python 3.11**。

若仍报错，请 **删除该 App 后重新部署**，在 **Advanced settings** 里把 Python version 选为 **3.11**（不能改已部署 App 的 Python 版本）。

参考：[Streamlit 论坛 - Python 3.14 与 TensorFlow](https://discuss.streamlit.io/t/streamlit-cloud-forcing-python-3-14-before-tensorflow-supports-it/121567)

### 3. MNIST 一直 “Running…” / 内存不足

Streamlit 免费 tier 内存有限；`tensorflow-cpu` 首次加载较慢，多等几分钟。若反复失败，可换时段重试或删掉 App 重新 Deploy。

### 4. 画板组件报错

`environment.yml` 中需包含 `streamlit-drawable-canvas`（已配置）。

### 5. 想用 Gitee 而不是 GitHub

Streamlit Cloud **官方只支持 GitHub**。可先把 Gitee 镜像同步到 GitHub，再按上文部署。

### 6. 本地前后端分离版（FastAPI + frontend）

云端 **不推荐** 跑两个服务；作业展示用 **`app.py` 单体版** 即可。本地仍可用 `backend.py` + `frontend.py` 演示架构。

---

## 六、更新线上版本

改代码后：

```powershell
git add -A
git commit -m "update apps"
git push
```

Streamlit Cloud 会自动重新部署（可在网页上看到 “Redeploying”）。

---

## 七、目录结构（部署相关）

```
Week5_Practice/
├── DEPLOY_STREAMLIT.md          ← 本说明
├── machine_learning_web_app/
│   ├── app.py                   ← MNIST 云端入口
│   ├── preprocess.py
│   ├── mnist.hdf5
│   ├── environment.yml
│   └── .python-version
└── ufo_project/
    ├── app.py                   ← UFO 云端入口
    ├── ufo-model.pkl
    └── requirements.txt
```
