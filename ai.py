# # write by chuan.sun on 2017/07/03
# import tensorflow as tf
#
# a = tf.constant([1, 2], name='a')
# b = tf.constant([3, 4], name='b')
# hello = tf.constant('Hello, TensorFlow!')
# # result = tf.add(a, b, name='add')
#
# # allow_soft_placement用来自动分配GPU和CPU任务，log_device_placement用来产生日志，在生产环境可以关闭，减少日志的产生量
# config = tf.ConfigProto(allow_soft_placement=True, log_device_placement=True)
#
# with tf.Session(config=config) as sess:
#     print(sess.run(hello))
#     print(a.eval())
# # tf.nn.softmax_cross_entropy_with_logits()
# # tf.nn.sparse_softmax_cross_entropy_with_logits()
#
#
# writer = tf.summary.FileWriter('path/t0/log',tf.get_default_graph())
# writer.close()


for x in range(1,10):
    print(x)
print(x); print(y)