from django.conf import settings
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from .models import Profile
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django.http.response import HttpResponseForbidden
from .models import History, Expense
from django.core.mail import send_mail


updating_balance = False


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.get_or_create(user=instance)  # sử dụng key được sinh ra


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.get_or_create(user=instance)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


@receiver(post_save, sender=History)
def update_balance(sender, instance, **kwargs):
    global updating_balance
    if updating_balance:
        return  # Ngăn chặn đệ quy

    # Bắt đầu tính toán balance
    try:
        updating_balance = True  # Đặt cờ để signal không kích hoạt lại

        # Lấy Expense tương ứng với user và tháng/năm
        expense = Expense.objects.filter(
            user=instance.user,
            date__year=instance.date.year,
            date__month=instance.date.month,
        ).first()

        if not expense:
            return  # Nếu không có Expense, thoát

        # Xác định trường cần cập nhật
        if instance.field == "R":
            field_value = expense.rent
        elif instance.field == "F":
            field_value = expense.food
        elif instance.field == "S":
            field_value = expense.saving
        elif instance.field == "O":
            field_value = expense.other
        else:
            field_value = None

        if field_value is not None:
            # Tính toán balance và cập nhật vào instance
            instance.balance = field_value - instance.amount
            # Sử dụng `update()` để tránh kích hoạt signal
            History.objects.filter(id=instance.id).update(balance=instance.balance)
    finally:
        updating_balance = False  # Đặt lại cờ sau khi hoàn tất


@receiver(post_save, sender=History)
def check_balance_after_history_creation(sender, instance, created, **kwargs):
    """
    Signal to check the balance from the latest History before creating a new History record.
    """
    if created:  # Chỉ xử lý khi một History mới được tạo
        # Lấy lịch sử gần nhất (ID lớn nhất) của cùng user
        last_history = History.objects.filter(user=instance.user).order_by('-id').first()

        # Nếu không có History trước đó, khởi tạo balance từ Expense
        if last_history is None:
            # Lấy thông tin Expense tương ứng
            try:
                expense = Expense.objects.get(user=instance.user)
            except Expense.DoesNotExist:
                # Nếu không có Expense, không thực hiện thêm
                return

            # Khởi tạo balance từ tổng số tiền trong Expense
            initial_balance = sum(
                filter(None, [expense.rent, expense.food, expense.saving, expense.other])
            )
        else:
            # Sử dụng balance từ History gần nhất
            initial_balance = last_history.balance

        # Tính balance sau khi trừ amount
        new_balance = initial_balance - instance.amount
        # instance.balance = new_balance  # Cập nhật balance cho History mới
        # instance.save()

        # Gửi email nếu balance <= 0
        if new_balance <= 0:
            send_email_to_user(instance.user.email, "Số dư của bạn đã đạt hoặc vượt mức giới hạn!")
        # expense.save()


updating_balance = False

def send_email_to_user(email,body):
    try:
        # Lấy đối tượng user từ database
        # Gửi email tới user.email
        send_mail(
            'Subject Balance fluctuation',  # Tiêu đề email
            body,  # Nội dung email
            settings.EMAIL_HOST_USER,  # Địa chỉ email gửi (được cấu hình trong settings.py)
            [email],  # Danh sách người nhận, ở đây là email của người dùng
            fail_silently=False,  # Nếu có lỗi thì sẽ ném ra ngoại lệ
        )
        print(f"Email sent to {email}")
    except User.DoesNotExist as e:
        print(e)