import json
from unittest.mock import patch

from django.test import SimpleTestCase

from .catalog import PRODUCTS, search_products
from .services import run_product_search


class ProductSearchTests(SimpleTestCase):
    def test_catalog_has_at_least_ten_of_each_product_type(self):
        self.assertGreaterEqual(sum(item["category"] == "laptop" for item in PRODUCTS), 10)
        self.assertGreaterEqual(sum(item["category"] == "mobile" for item in PRODUCTS), 10)

    def test_search_matches_category_price_and_ram(self):
        results = search_products(category="laptop", max_price=50000, ram="16GB")

        self.assertTrue(results)
        self.assertTrue(all(item["category"] == "laptop" for item in results))
        self.assertTrue(all(item["price"] <= 50000 for item in results))
        self.assertTrue(all(item["ram"] == "16GB" for item in results))

    def test_lenovo_laptop_returns_only_lenovo_laptops(self):
        results = search_products(category="laptop", brand="Lenovo")

        self.assertEqual({item["brand"] for item in results}, {"Lenovo"})
        self.assertTrue(all(item["category"] == "laptop" for item in results))

    def test_acer_laptop_returns_only_acer_laptops(self):
        results = search_products(category="laptop", brand="Acer")

        self.assertEqual({item["brand"] for item in results}, {"Acer"})
        self.assertTrue(all(item["category"] == "laptop" for item in results))

    def test_laptop_under_50000_respects_price_limit(self):
        results = search_products(category="laptop", max_price=50000)

        self.assertTrue(results)
        self.assertTrue(all(item["category"] == "laptop" and item["price"] <= 50000 for item in results))

    def test_lenovo_laptop_under_50000_matches_all_filters(self):
        results = search_products(category="laptop", brand="Lenovo", max_price=50000)

        self.assertTrue(results)
        self.assertTrue(all(item["brand"] == "Lenovo" and item["price"] <= 50000 for item in results))

    def test_mobile_under_20000_respects_price_limit(self):
        results = search_products(category="mobile", max_price=20000)

        self.assertTrue(results)
        self.assertTrue(all(item["category"] == "mobile" and item["price"] <= 20000 for item in results))

    def test_samsung_mobile_with_8gb_ram_matches_all_filters(self):
        results = search_products(category="mobile", brand="Samsung", ram="8GB")

        self.assertTrue(results)
        self.assertTrue(all(item["brand"] == "Samsung" and item["ram"] == "8GB" for item in results))

    def test_black_laptop_returns_only_black_laptops(self):
        results = search_products(category="laptop", color="black")

        self.assertTrue(results)
        self.assertTrue(all(item["category"] == "laptop" and "black" in item["color"].casefold() for item in results))

    def test_no_matching_products_returns_empty_list(self):
        results = search_products(category="laptop", brand="Lenovo", max_price=1000)

        self.assertEqual(results, [])

    @patch("products.services.ask_openrouter")
    def test_tool_call_returns_only_matching_brand_products(self, ask_mock):
        ask_mock.side_effect = [
            {
                "tool_calls": [
                    {
                        "id": "call-1",
                        "function": {
                            "name": "search_products",
                            "arguments": '{"category":"laptop","brand":"Lenovo"}',
                        },
                    }
                ]
            },
            {"content": "I found Lenovo laptops."},
        ]

        result = run_product_search("lenovo laptop")

        self.assertTrue(result["products"])
        self.assertTrue(all(item["brand"] == "Lenovo" for item in result["products"]))
        properties = ask_mock.call_args_list[0].kwargs["tools"][0]["function"]["parameters"]["properties"]
        self.assertIn("brand", properties)
        sent_to_ai = json.loads(ask_mock.call_args_list[1].args[0][-1]["content"])
        self.assertTrue(all(item["brand"] == "Lenovo" for item in sent_to_ai))

    def test_search_matches_mobile_storage_and_color(self):
        results = search_products(category="mobiles", max_price=25000, storage="256GB", color="black")

        self.assertTrue(results)
        self.assertTrue(all(item["category"] == "mobile" for item in results))
        self.assertTrue(all(item["storage"] == "256GB" for item in results))
        self.assertTrue(all("black" in item["color"].casefold() for item in results))

    def test_search_endpoint_rejects_empty_message(self):
        response = self.client.post("/api/products/search/", {"message": " "}, content_type="application/json")

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["error"], "Please enter what you are looking for.")

    @patch("products.views.run_product_search")
    def test_search_endpoint_returns_message_and_products(self, search_mock):
        search_mock.return_value = {
            "message": "I found one laptop.",
            "products": [{"name": "Acer Aspire 5", "price": 47999}],
        }

        response = self.client.post(
            "/api/products/search/",
            {"message": "Show me a laptop"},
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), search_mock.return_value)