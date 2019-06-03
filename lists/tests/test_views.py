from django.test import TestCase
from django.urls import resolve
from lists.views import home_page
from django.http import HttpRequest
from lists.models import Item, List
from django.utils.html import escape
from lists.forms import ItemForm

# Create your tests here.


class HomePageTest(TestCase):

    def test_uses_home_template(self):
        response = self.client.get('/')
        self.assertContains(response, 'To-Do')
        self.assertTemplateUsed(response, 'home.html')

    def test_home_page_use_item_form(self):
        response = self.client.get('/')
        self.assertIsInstance(response.context['form'], ItemForm)

class ListViewTest(TestCase):

    def test_user_list_template(self):
        list_ = List.objects.create()
        response = self.client.get(f'/lists/{list_.id}/')
        self.assertTemplateUsed(response, 'list.html')

    def test_display_all_lists_items(self):
        correct_list_ = List.objects.create()
        Item.objects.create(text='itemey 1', list=correct_list_)
        Item.objects.create(text='itemey 2', list=correct_list_)

        other_list_ = List.objects.create()
        Item.objects.create(text='other list item 1', list=other_list_)
        Item.objects.create(text='other list item 2', list=other_list_)

        response = self.client.get(f'/lists/{correct_list_.id}/')

        self.assertContains(response, 'itemey 1')
        self.assertContains(response, 'itemey 2')
        self.assertNotContains(response, 'other list item 1')
        self.assertNotContains(response, 'other list item 2')

    def test_passes_correct_list_to_template(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        response = self.client.get(f'/lists/{correct_list.id}/')
        self.assertEqual(response.context['list'], correct_list)

    def test_can_save_a_POST_requests_to_an_existing_list(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        self.client.post(f'/lists/{correct_list.id}/', data={'item_text': 'A new item for an existing list'})

        # 测试事项是否保存
        self.assertEqual(Item.objects.count(), 1)

        # 测试数据库中事项为上述新增事项
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new item for an existing list')

        # 测试该新增事项被添加到了目标清单中
        self.assertEqual(new_item.list, correct_list)

    def test_POST_redirects_to_list_view(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.post(f'/lists/{correct_list.id}/',
                                    data={'item_text': 'A new item for an existing list'})
        self.assertRedirects(response, f'/lists/{correct_list.id}/')

    def test_validation_errors_end_up_on_lists_page(self):
        list_ = List.objects.create()
        response = self.client.post(
            f'/lists/{list_.id}/', data={'item_text': ''}
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'list.html')
        expected_error = escape("You can't have an empty list item")
        self.assertContains(response, expected_error)

class NewListTest(TestCase):

    def test_can_save_a_POST_request(self):
        response = self.client.post('/lists/new', data={'item_text': 'A new list item'})

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')

    def test_redirects_after_POST(self):
        response = self.client.post('/lists/new', data={'item_text': 'A new list item'})
        new_list = List.objects.first()
        # self.assertEqual(response.status_code, 302)
        # self.assertEqual(response['location'], '/lists/the-only-list-in-the-world/')
        ## assertRedirects 可以代替上面两行
        self.assertRedirects(response, f'/lists/{new_list.id}/')

    def test_validation_errors_are_sent_back_to_home_page_template(self):
        response = self.client.post('/lists/new', data={'item_text': ''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        expected_error = escape("You can't have an empty list item")
        # print(response.content.decode())
        # print(expected_error)
        self.assertContains(response, expected_error)

    def test_invaild_list_items_arent_saved(self):
        self.client.post('/lists/new', data={'item_text': ''})
        self.assertEqual(List.objects.count(), 0)
        self.assertEqual(Item.objects.count(), 0)


# class NewItemTest(TestCase):




