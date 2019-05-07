from django.core.files.storage import Storage
# 先导入我们安装的 fdfs_client.client 客户端
from fdfs_client.client import Fdfs_client
# 导入 settings 文件
from django.conf import settings


# 创建 fastdfs文件存储类:
class FastDFSStorage(Storage):
    # name: 用户选择上传文件的名称
    #  content: 含有上传文件内容的一个File对象,
    #  我们可以通过content.read(), 获取上传文件的内容
    def save(self, name, content, max_length=None):
        '''重写上传文件的函数'''

        # 我们需要将文件上传到 FastDFS 上面.
        # 创建客户端对象:
        client = Fdfs_client(settings.FDFS_CLIENT_CONF)

        # 调用上传函数, 进行上传:
        # 我们这里调用的是上面说过的, 根据文件内容上传方法.
        result = client.upload_by_buffer(content.read())

        # 判断是否上传成功:
        if result.get('Status') == 'Upload successed.':
            # 上传成功: 返回 file_id:
            file_id = result.get('Remote file_id')

            # 这个位置返回以后, django 自动会给我们保存到表字段里.
            return file_id

        else:

            # 上传失败
            raise Exception('上传文件到FDFS系统失败')

    def exists(self, name):

        # 判断当前要传入的图片是否已经存在
        # fdfs 中的文件名是由 fdfs 生成的, 所以不可能冲突
        # 我们返回 False: 永不冲突
        return False

    def url(self, name):

        # 返回可访问到文件的完整的url地址
        # 保存成功后, 返回的图片是不完整的,拼接完整
        return settings.FDFS_URL + name