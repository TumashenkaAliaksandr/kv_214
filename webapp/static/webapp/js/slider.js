document.addEventListener("DOMContentLoaded", () => {
    // Главный слайдер
    let slideIndex = 0;
    const slides = document.querySelectorAll(".slider-main .slide");
    const totalSlides = slides.length;

    function showSlide(index) {
        const slidesContainer = document.querySelector(".slider-main .slides");
        const sliderWrapper = document.querySelector(".slider-main .slider-wrapper");
        const slide = slides[0];

        const windowWidth = window.innerWidth;

        if (windowWidth <= 768) {
            // Мобильные - считаем сдвиг в пикселях по ширине слайда и центруем
            const slideWidth = slide.offsetWidth;
            const wrapperWidth = sliderWrapper.offsetWidth;
            // Центрируем слайд по середине wrapper, сдвигая slides влево
            // Формула: смещение = slideWidth * index - (wrapperWidth - slideWidth)/2
            const offset = slideWidth * index - (wrapperWidth - slideWidth) / 2;

            slidesContainer.style.transform = `translateX(${-offset}px)`;
        } else {
            // Десктоп - двигаемся на 100% слайда ширины (как было)
            slidesContainer.style.transform = `translateX(${-index * 100}%)`;
        }
    }


    function nextSlide() {
        slideIndex = (slideIndex + 1) % totalSlides;
        showSlide(slideIndex);
    }

    setInterval(nextSlide, 4000);
    showSlide(slideIndex);
    //ТОп объекты слайдер
    const newObjectsWrapper = document.querySelector(".slider-new-objects .new-objects-wrapper");
    const newObjects = document.querySelector(".slider-new-objects .new-objects");
    const newObjectsLeftBtn = document.querySelector(".slider-new-objects .left-arrow");
    const newObjectsRightBtn = document.querySelector(".slider-new-objects .right-arrow");

    let posNewObjects = 0;
    let newObjectElement = newObjects.querySelector(".new-object");
    const gapNew = 16;

    function updateVisibleCountNew() {
        const containerWidthNew = newObjectsWrapper.offsetWidth;
        const itemWidthNew = newObjectElement.offsetWidth + gapNew;
        const visibleCount = Math.floor(containerWidthNew / itemWidthNew);
        return visibleCount > 0 ? visibleCount : 1; // минимум 1
    }

    function updateSizes() {
        newObjectElement = newObjects.querySelector(".new-object");
        const itemWidthNew = newObjectElement.offsetWidth + gapNew;
        const visibleCountNew = updateVisibleCountNew();
        let maxShiftNew = itemWidthNew * (newObjects.children.length - visibleCountNew);
        if (maxShiftNew < 0) maxShiftNew = 0;
        return {itemWidthNew, visibleCountNew, maxShiftNew};
    }

    let {itemWidthNew, visibleCountNew, maxShiftNew} = updateSizes();

    function slideTo(position) {
        posNewObjects = position;
        newObjects.style.transform = `translateX(${posNewObjects}px)`;
    }

    newObjectsLeftBtn.addEventListener("click", () => {
        if (posNewObjects < 0) {
            slideTo(posNewObjects + itemWidthNew);
        } else {
            slideTo(-maxShiftNew);
        }
    });

    newObjectsRightBtn.addEventListener("click", () => {
        if (posNewObjects > -maxShiftNew) {
            slideTo(posNewObjects - itemWidthNew);
        } else {
            slideTo(0);
        }
    });

    window.addEventListener("resize", () => {
        let sizes = updateSizes();
        itemWidthNew = sizes.itemWidthNew;
        visibleCountNew = sizes.visibleCountNew;
        maxShiftNew = sizes.maxShiftNew;
        slideTo(0);
    });

// Автоплей слайдера
    setInterval(() => {
        newObjectsRightBtn.click();
    }, 5000);


    // Второй слайдер (обратный)
    const objectsWrapper = document.querySelector(".slider-objects-reverse .objects-wrapper");
    const objects = document.querySelector(".slider-objects-reverse .objects");
    const objectsLeftBtn = document.querySelector(".slider-objects-reverse .left-arrow");
    const objectsRightBtn = document.querySelector(".slider-objects-reverse .right-arrow");

    let posObjects = 0;
    const objectElement = objects.querySelector(".object-item");
    const gapObjects = 16;
    let itemWidthObjects = objectElement.offsetWidth + gapObjects;

    function updateVisibleCountObjects() {
        itemWidthObjects = objectElement.offsetWidth + gapObjects;
        const containerWidthObjects = objectsWrapper.offsetWidth;
        return Math.floor(containerWidthObjects / itemWidthObjects);
    }

    let visibleCountObjects = updateVisibleCountObjects();
    let maxShiftObjects = itemWidthObjects * (objects.children.length - visibleCountObjects);
    if (maxShiftObjects < 0) maxShiftObjects = 0;

    objectsLeftBtn.addEventListener("click", () => {
        if (posObjects > -maxShiftObjects) {
            posObjects -= itemWidthObjects;
            if (posObjects < -maxShiftObjects) posObjects = -maxShiftObjects;
            objects.style.transform = `translateX(${posObjects}px)`;
        } else {
            posObjects = 0;
            objects.style.transform = `translateX(0px)`;
        }
    });

    objectsRightBtn.addEventListener("click", () => {
        if (posObjects < 0) {
            posObjects += itemWidthObjects;
            if (posObjects > 0) posObjects = 0;
            objects.style.transform = `translateX(${posObjects}px)`;
        } else {
            posObjects = -maxShiftObjects;
            objects.style.transform = `translateX(${posObjects}px)`;
        }
    });

    // Автоплей в другую сторону
    setInterval(() => {
        objectsLeftBtn.click();
    }, 5000);

    // Обновление размеров на ресайз
    window.addEventListener("resize", () => {
        visibleCountNew = updateVisibleCountNew();
        maxShiftNew = itemWidthNew * (newObjects.children.length - visibleCountNew);
        if (maxShiftNew < 0) maxShiftNew = 0;
        if (posNewObjects < -maxShiftNew) {
            posNewObjects = -maxShiftNew;
            newObjects.style.transform = `translateX(${posNewObjects}px)`;
        }

        visibleCountObjects = updateVisibleCountObjects();
        maxShiftObjects = itemWidthObjects * (objects.children.length - visibleCountObjects);
        if (maxShiftObjects < 0) maxShiftObjects = 0;
        if (posObjects < -maxShiftObjects) {
            posObjects = -maxShiftObjects;
            objects.style.transform = `translateX(${posObjects}px)`;
        }
    });
});
