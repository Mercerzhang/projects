from django.contrib.auth.models import AbstractUser
from django.db import models
from itsdangerous import TimedJSONWebSignatureSerializer, BadData
from django.conf import settings

from meiduo_mall.utils.BaseModel import BaseModel


# 我们重写用户模型类, 继承自 AbstractUser
class User(AbstractUser):
    """自定义用户模型类"""

    # 在用户模型类中增加 mobile 字段
    # models.CharField这个位置指出了当前字段的类型:
    mobile = models.CharField(max_length=11, unique=True, verbose_name='手机号')

    # 新增 email_active 字段
    # 用于记录邮箱是否激活, 默认为 False: 未激活
    email_active = models.BooleanField(default=False, verbose_name='邮箱验证状态')

    # 新增默认地址字段
    default_address = models.ForeignKey(
        'Address',
        related_name='users',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name='默认地址')

    # 对当前表进行相关设置:
    class Meta:
        db_table = 'tu_users'  # 指明数据库表名
        verbose_name = '用户'  # 在admin站点中显示的名称
        verbose_name_plural = verbose_name  # 显示的复数名称

    # 在 str 魔法方法中, 返回用户名称
    def __str__(self):
        """定义每个数据对象的显示信息"""
        return self.username

    def generate_verify_email_url(self):
        """
           生成邮箱验证链接，生成加密token函数
           :param user: 当前登录用户
           :return: verify_url
           """

        # 调用 itsdangerous 中的类,生成对象
        # 有效期: 1天
        serializer = TimedJSONWebSignatureSerializer(settings.SECRET_KEY, expires_in=60 * 60 * 24)

        # 拼接参数
        data = {
            'user_id':self.id,
            'email':self.email,
        }

        # 生成 token 值, 这个值是 bytes 类型, 所以解码为 str:
        token = serializer.dumps(data).decode()

        # 拼接url
        verify_url = settings.EMAIL_VERIFY_URL + '?token=' + token

        # 返回
        return verify_url


    # 定义验证函数:
    @staticmethod
    def check_verify_email_token(token):
        """
            解密，验证token并提取user
            :param token: 用户信息签名后的结果
            :return: user, None
            """
        # 调用 itsdangerous 类,生成对象
        # 邮件验证链接有效期：一天
        serializer = TimedJSONWebSignatureSerializer(settings.SECRET_KEY, expires_in=3600 * 24)

        try:
            # 解秘传入的 token 值, 获取数据 data
            data = serializer.loads(token)

        except BadData:
            # 如果传入的 token 中没有值, 则报错
            return None

        else:
            #  如果有值, 则获取
            user_id = data.get('user_id')
            email = data.get('email')

        try:
            # 获取到值之后, 尝试从 User 表中获取对应的用户
            user = User.objects.get(id=user_id, email=email)

        except User.DoesNotExist:
            # 如果用户不存在, 则返回 None
            return None

        else:
            # 如果存在则直接返回
            return user


class Address(BaseModel):
    """
    用户地址
    """
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='addresses',
                             verbose_name='用户')

    province = models.ForeignKey('areas.Area',
                                 on_delete=models.PROTECT,
                                 related_name='province_addresses',
                                 verbose_name='省')

    city = models.ForeignKey('areas.Area',
                             on_delete=models.PROTECT,
                             related_name='city_addresses',
                             verbose_name='市')

    district = models.ForeignKey('areas.Area',
                                 on_delete=models.PROTECT,
                                 related_name='district_addresses',
                                 verbose_name='区')

    title = models.CharField(max_length=20, verbose_name='地址名称')
    receiver = models.CharField(max_length=20, verbose_name='收货人')
    place = models.CharField(max_length=50, verbose_name='地址')
    mobile = models.CharField(max_length=11, verbose_name='手机')
    tel = models.CharField(max_length=20,
                           null=True,
                           blank=True,
                           default='',
                           verbose_name='固定电话')

    email = models.CharField(max_length=30,
                             null=True,
                             blank=True,
                             default='',
                             verbose_name='电子邮箱')

    is_deleted = models.BooleanField(default=False, verbose_name='逻辑删除')

    class Meta:
        db_table = 'tb_address'
        verbose_name = '用户地址'
        verbose_name_plural = verbose_name
        ordering = ['-update_time']
