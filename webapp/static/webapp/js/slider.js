/*
  Простейший автослайдер для главного слайдера
  и слайдеров новых объектов и обратный слайдер объектов
  c автолуппом и автоплеем.
*/

document.addEventListener("DOMContentLoaded", () => {
  // Главный слайдер
  let slideIndex = 0;
  const slides = document.querySelectorAll(".slider-main .slide");
  const totalSlides = slides.length;

  function showSlide(index) {
    const slidesContainer = document.querySelector(".slider-main .slides");
    slidesContainer.style.transform = `translateX(${-index * 100}%)`;
  }

  function nextSlide() {
    slideIndex = (slideIndex + 1) % totalSlides;
    showSlide(slideIndex);
  }

  setInterval(nextSlide, 4000);
  showSlide(slideIndex);

  // Слайдер Новые объекты
  const newObjectsWrapper = document.querySelector(".slider-new-objects .new-objects-wrapper");
  const newObjects = document.querySelector(".slider-new-objects .new-objects");
  const newObjectsLeftBtn = document.querySelector(".slider-new-objects .left-arrow");
  const newObjectsRightBtn = document.querySelector(".slider-new-objects .right-arrow");

  let posNewObjects = 0;
  const itemWidthNew = newObjects.querySelector(".new-object").offsetWidth + 16; // gap

  newObjectsLeftBtn.addEventListener("click", () => {
    if (posNewObjects < 0) {
      posNewObjects += itemWidthNew;
      newObjects.style.transform = `translateX(${posNewObjects}px)`;
    } else {
      // зациклить в конец
      posNewObjects = -(itemWidthNew * (newObjects.children.length - 5));
      newObjects.style.transform = `translateX(${posNewObjects}px)`;
    }
  });

  newObjectsRightBtn.addEventListener("click", () => {
    if (posNewObjects > -(itemWidthNew * (newObjects.children.length - 5))) {
      posNewObjects -= itemWidthNew;
      newObjects.style.transform = `translateX(${posNewObjects}px)`;
    } else {
      posNewObjects = 0;
      newObjects.style.transform = `translateX(0px)`;
    }
  });

  // Автоплей для новых объектов
  setInterval(() => {
    newObjectsRightBtn.click();
  }, 5000);

  // Второй слайдер (обратный)
  const objectsWrapper = document.querySelector(".slider-objects-reverse .objects-wrapper");
  const objects = document.querySelector(".slider-objects-reverse .objects");
  const objectsLeftBtn = document.querySelector(".slider-objects-reverse .left-arrow");
  const objectsRightBtn = document.querySelector(".slider-objects-reverse .right-arrow");

  let posObjects = 0;
  const itemWidthObjects = objects.querySelector(".object-item").offsetWidth + 16; // gap

  objectsLeftBtn.addEventListener("click", () => {
    if (posObjects > -(itemWidthObjects * (objects.children.length - 5))) {
      posObjects -= itemWidthObjects;
      objects.style.transform = `translateX(${posObjects}px)`;
    } else {
      posObjects = 0;
      objects.style.transform = `translateX(0px)`;
    }
  });

  objectsRightBtn.addEventListener("click", () => {
    if (posObjects < 0) {
      posObjects += itemWidthObjects;
      objects.style.transform = `translateX(${posObjects}px)`;
    } else {
      posObjects = -(itemWidthObjects * (objects.children.length - 5));
      objects.style.transform = `translateX(${posObjects}px)`;
    }
  });

  // Автоплей в другую сторону
  setInterval(() => {
    objectsLeftBtn.click();
  }, 5000);

});
