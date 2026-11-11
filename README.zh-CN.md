# 控制回路延迟实验台

研究控制指令延迟如何改变 PID 电机位置系统的阶跃响应。

这是一个可复现的**仿真起步项目**，不依赖第三方 Python 包，可输出 CSV 数据、JSON 指标和 SVG 曲线。仿真结果不是实机测量；接入电机与编码器后，才能把结果称为真机数据。

## 快速运行

```bash
python -m control_delay_lab --delays-ms 0,50,100,150,200 --out results
```

程序会在 `results/` 生成 `results.csv`、`summary.json` 和 `response.svg`。指标包括超调量、调节时间、最终误差、峰值位置和稳定状态标签。

## 模型与限制

仿真包含位置、速度、惯量、阻尼、执行器饱和、固定采样周期和 FIFO 指令延迟队列。默认参数仅用于说明，未根据具体电机辨识。发布结果时请同时提供参数和原始 CSV，不要把仿真描述为实测。

Python 3.10 或更高版本，无第三方依赖。硬件接入方案见 [`docs/hardware-adapter.md`](docs/hardware-adapter.md)。

## License

MIT，见 `LICENSE`。

