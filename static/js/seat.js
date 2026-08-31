const seats = document.querySelectorAll(".seat");

const selectedSeat = document.getElementById(
    "selected-seat"
);


seats.forEach(seat => {

    seat.addEventListener("click", () => {

        // Bỏ chọn tất cả ghế
        seats.forEach(s => {
            s.classList.remove("selected");
        });


        // Chọn ghế hiện tại
        seat.classList.add("selected");


        // Hiển thị ghế đã chọn
        selectedSeat.textContent =
            seat.dataset.seat;

    });

});