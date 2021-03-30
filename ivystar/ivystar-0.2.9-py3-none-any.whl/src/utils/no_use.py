#!
import tensorflow as tf
import tensorflow_datasets as tfds

dataset, metadata = tfds.load('fashion_mnist', as_supervised=True, with_info=True)
print(metadata)
train_dataset, test_dataset = dataset['train'], dataset['test']
train_dataset = train_dataset.shuffle(100).batch(12).repeat()

for img, label in train_dataset.take(1):
    img = img.numpy()
    print(img.shape)
    print(img)
