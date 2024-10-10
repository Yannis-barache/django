from django.urls import path
from . import views

urlpatterns = [
    path('product/list', views.ProductListView.as_view(), name='Tous les produits'),
    path('contact', views.ContactView, name='Contact'),
    path('about', views.About, name='About'),
    path('search/', views.search_view, name='search'),
    path('email-sent', views.EmailSent, name='email-sent'),
    path('product/<pk>', views.ProductDetailView.as_view(), name='detail_produit'),
    path('product_attribute/list', views.ProductAttributeListView.as_view(), name='attribute-list'),

    path('login/', views.ConnectView.as_view(), name='connexion'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('logout/', views.DisconnectView.as_view(), name='logout'),
    #path("product/add/",views.ProductCreate, name="product-add"),
    path("product/add/",views.ProductCreateView.as_view(), name="product-add"),
    path("product/<pk>/update/",views.ProductUpdateView.as_view(), name="product-update"),
    path("product/<pk>/delete/", views.ProductDeleteView.as_view(), name="product-delete"),

    path("product_attribute/<pk>",views.ProductAttributeDetailView.as_view(), name="attribute-detail"),

    path("product_attribute/add/",views.ProductAttributeCreateView.as_view(), name="attribute-create"),
    path("product_attribute/<pk>/update/",views.ProductAttributeUpdateView.as_view(), name="attribute-update"),
    path("product_attribute/<pk>/delete/", views.ProductAttributeDeleteView.as_view(), name="attribute-delete"),

    path('product_item/list', views.ProductItemListView.as_view(), name='item-list'),
    path('product_item/<pk>', views.ProductItemDetailView.as_view(), name='item-detail'),
    path('product_item/add/', views.ProductItemCreateView.as_view(), name='item-create'),
    path('product_item/<pk>/update/', views.ProductItemUpdateView.as_view(), name='item-update'),
    path('product_item/<pk>/delete/', views.ProductItemDeleteView.as_view(), name='item-delete'),


    path('supplier/list', views.SupplierListView.as_view(), name='supplier-list'),
    path('supplier/<pk>', views.supplier_detail, name='supplier-detail'),
    path('supplier/add/', views.SupplierCreateView.as_view(), name='supplier-create'),
    path('supplier/<pk>/update/', views.SupplierUpdateView.as_view(), name='supplier-update'),
    path('supplier/<pk>/delete/', views.SupplierDeleteView.as_view(), name='supplier-delete'),




]