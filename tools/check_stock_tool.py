from helpers.read_json_file import read_json_file

check_stock_tool_definition = {
    "type": "function",
    "name": "check_stock",
    "description": (
        "Allows the user to check the stock availability of a product in the e-commerce store. "
        "It returns the number of units available in stock for the specified product."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "product_name": {
                "type": "string",
                "description": "The name of the product for which stock availability is being checked."
            }
        },
        "required": ["product_name"]
    }
}

async def check_stock_tool(parameters):
    product_name = parameters.get('product_name')
    products = await read_json_file('../dummy_db/products.json')
    
    for product in products:
        if product['name'].lower() == product_name.lower():
            return {"result": f"The product {product_name} has {product['stock']} units in stock."}
    
    return {"result": f"The product {product_name} is not available."}
