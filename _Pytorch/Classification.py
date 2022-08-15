import torch
import matplotlib.pyplot as plt
import torch.nn.functional as F  # Activation Function
import numpy as np


if __name__ == '__main__':
    # 假數據
    n_data = torch.ones(100, 2)
    # 生成平均2, 標準差1的(100, 2)的Tensor
    x0 = torch.normal(mean=2*n_data, std=1)   # Class_0 x data, shape=(100, 2)
    y0 = torch.zeros(100)                     # Class_0 y data, shape=(100, )
    x1 = torch.normal(mean=-2*n_data, std=1)  # Class_1 x data, shape=(100, 1)
    y1 = torch.ones(100)                      # Class_1 y data, shape=(100, )

    # 注意 data 和 label 的數據形式一定要是跟下面一樣指定的dtype
    # torch.cat 合併數據, dim=0 ---> 上下合併, dim=1 ---> 左右合併
    # FloatTensor = 32-bit floating(x.dtype ---> torch.float32), shape=(200, 2)
    x = torch.cat((x0, x1), dim=0).type(torch.FloatTensor)
    # LongTensor = 64-bit integer(y.dtype ---> torch.int64), shape=(200, )
    y = torch.cat((y0, y1), dim=0).type(torch.LongTensor)
    # # 假數據最初的圖
    # plt.scatter(x.data.numpy()[:, 0], x.data.numpy()[:, 1], c=y.data.numpy(), s=100, lw=0, cmap='RdYlGn')
    # plt.show()

    class Net(torch.nn.Module):  # 繼承 torch 的 Module(官方文件建議寫法)
        def __init__(self, n_feature, n_hidden, n_output):
            super(Net, self).__init__()  # 繼承
            # super().__init__()  # 在python3中可以改寫為這種寫法
            # 定義神經網路的結構
            self.hidden = torch.nn.Linear(n_feature, n_hidden)  # 輸入和輸出的神經元個數
            self.out = torch.nn.Linear(n_hidden, n_output)      # 輸入和輸出的神經元個數

        def forward(self, x):
            # x為 input data
            hidden_x = F.relu(self.hidden(x))  # 過一層Activation Function ---> 隱藏層的輸出
            out_x = self.out(hidden_x)         # 輸出層的輸出
            return out_x

    # Fully-Connected Network
    net = Net(2, 10, 2)  # 分類問題, 兩個特徵(一個座標點有x, y兩個特徵), 兩個類別 ---> 兩個輸出

    # # method2, 也可以使用Sequential快速地搭建神經網路, 效果同上
    # net2 = torch.nn.Sequential(
    #     torch.nn.Linear(2, 10),
    #     torch.nn.ReLU(),
    #     torch.nn.Linear(10, 2)
    # )

    optimizer = torch.optim.SGD(net.parameters(), lr=0.02)  # 傳入net的參數, learning rate
    loss_func = torch.nn.CrossEntropyLoss()
    plt.ion()
    plt.show()
    for t in range(100):
        out = net(x)              # 傳入training data開始訓練
        loss = loss_func(out, y)  # out---> 輸出值, y ---> label
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        if t % 2 == 0:
            plt.cla()
            # torch.max: dim=0 ---> 傳回每一行 [最大值], [index], dim=1 ---> 傳回每一列 [最大值], [index]
            # F.softmax(out, dim=1): dim=0 ---> 每一行取softmax, dim=1 ---> 每一列取softmax
            prediction = torch.max(F.softmax(out, dim=1), dim=1)[1]  # 取機率高的那個(類別 ---> index)
            y_predict = prediction.data.numpy()
            y_target = y.data.numpy()  # y label
            # 畫出原本的點, 顏色以y_predict標示, 而非以y_label標示
            plt.scatter(x.data.numpy()[:, 0], x.data.numpy()[:, 1], c=y_predict, s=100, lw=0, cmap='RdYlGn')
            # np.sum(y_predict == target_y) ---> True當1, False當0, 加起來
            accuracy = np.sum(y_predict == y_target) / 200.  # 預測準確率, 在training data上的準確率
            plt.text(1.5, -4, 'Accuracy=%.2f' % accuracy, fontdict={'size': 20, 'color': 'red'})
            plt.pause(0.1)

    plt.ioff()
    plt.show()
