from keras.datasets import mnist
from keras import models, layers
from keras.utils import to_categorical
import matplotlib.pyplot as plt

# 加载keras中的MNIST数据集
(train_images, train_labels), (test_images, test_labels) = mnist.load_data()
print(train_images.shape)
print(len(train_labels))
print(test_images.shape)
print(len(test_labels))


#显示数据集中第四个数字
digit = train_images[4]
plt.imshow(digit, cmap=plt.cm.binary)
plt.show()


# 网络架构
network = models.Sequential()
network.add(layers.Dense(512, activation='relu', input_shape=(28 * 28,)))
network.add(layers.Dense(10, activation='softmax'))

# 编译过程
# 训练网络，需要选择编译步骤的三个参数：1.损失函数 2.优化器 3.指标
network.compile(optimizer='rmsprop', loss='categorical_crossentropy', metrics=['accuracy'])

# 准备图像数据
train_images = train_images.reshape((60000, 28 * 28))
train_images = train_images.astype('float32') / 255

test_images = test_images.reshape((10000, 28 * 28))
test_images = test_images.astype('float32') / 255

# 准备标签
train_labels = to_categorical(train_labels)
test_labels = to_categorical(test_labels)

# 训练
network.fit(train_images, train_labels, epochs=3, batch_size=128)

# 测试
test_loss, test_acc = network.evaluate(test_images, test_labels)
print('test_acc:', test_acc)
