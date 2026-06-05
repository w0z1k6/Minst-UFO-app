# MNIST & UFO Streamlit Apps

Week 5 机器学习 Web 应用作业。

## 在线部署（Streamlit Cloud）

| 应用 | 入口文件 |
|------|----------|
| MNIST 手写数字识别 | `machine_learning_web_app/app.py` |
| UFO 目击国家预测 | `ufo_project/app.py` |

部署步骤见 [DEPLOY_STREAMLIT.md](DEPLOY_STREAMLIT.md)。

## 本地运行

```powershell
# MNIST
cd machine_learning_web_app
.\venv\Scripts\Activate.ps1
streamlit run app.py

# UFO
cd ufo_project
streamlit run app.py
```
