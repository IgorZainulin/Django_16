# from django.core.management.base import BaseCommand, CommandError
# from news.models import Post
#
#
# class Command(BaseCommand):
#     help = 'Обнуляет количество всех товаров'
#
#     def handle(self, *args, **kwargs):
#         for post in Post.objects.all():
#             post.quantity = 0
#             post.save()
#
#             self.stdout.write(self.style.SUCCESS('Successfully nulled product "%s"' % str(product)))


# from django.core.management.base import BaseCommand, CommandError
#
#
# class Command(BaseCommand):
#     help = 'Подсказка вашей команды'  # показывает подсказку при вводе "python manage.py <ваша команда> --help"
#     missing_args_message = 'Недостаточно аргументов'
#     requires_migrations_checks = True  # напоминать ли о миграциях. Если true — то будет напоминание о том, что не сделаны все миграции (если такие есть)
#
#     def add_arguments(self, parser):
#         # Positional arguments
#         parser.add_argument('argument', nargs='+', type=int)
#
#     def handle(self, *args, **options):
#         # здесь можете писать любой код, который выполняется при вызове вашей команды
#         self.stdout.write(str(options['argument']))

from django.core.management.base import BaseCommand, CommandError
from news.models import Post, Category


class Command(BaseCommand):
    help = 'Подсказка вашей команды'  # показывает подсказку при вводе "python manage.py <ваша команда> --help"
    requires_migrations_checks = True  # напоминать ли о миграциях. Если true — то будет напоминание о том, что не сделаны все миграции (если такие есть)

    def add_arguments(self, parser):
        parser.add_argument('category', type=str)


    def handle(self, *args, **options):
        answer = input(f'Вы правда хотите удалить все статьи в категории '
                       f'{options["category"]}? yes/no: ')


        if answer != 'yes':
            self.stdout.write(self.style.ERROR('Отменено'))
            return

        try:
            category = Category.objects.get(name=options['category'])
            Post.objects.filter(category=category).delete()
            self.stdout.write(self.style.SUCCESS(f'Succesfully deleted all news from '
                                                 f'category {category.name}'))

        except Category.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'Could not find category '
                                               f'{options['category']}'))



