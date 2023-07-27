// document.querySelectorAll('.product-card__buy-btn').forEach(async (btn) => {
//     btn.addEventListener('click', async () => {
//         const productID = btn.getAttribute("data-product");
//         const response = await request_json(`order_${productID}/`, null);

//         if (response.type === "success") {
//             const card = btn.closest('div.product-card');
//             btn.classList.add("disabled");
//             card.classList.add("bought");
//         }

//         showNotification(response.type, response.message);
//     });
// });

