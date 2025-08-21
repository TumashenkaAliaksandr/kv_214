// (function() {
//   const container = document.body;
//
//   function adjustScale() {
//     const width = window.innerWidth;
//     let scale = 1, fontScale = 1, paddingScale = 1;
//     let maxWidth = '100%';
//
//     if (width < 480) {       // Очень маленькие экраны (мобилки)
//       scale = 0.85;
//       fontScale = 0.85;
//       paddingScale = 0.75;
//       maxWidth = '350px';    // Ограничиваем ширину контейнера
//     } else if (width < 768) { // Мобилки
//       scale = 0.9;
//       fontScale = 0.9;
//       paddingScale = 0.85;
//       maxWidth = '600px';
//     } else if (width < 1024) { // Планшеты
//       scale = 0.95;
//       fontScale = 0.95;
//       paddingScale = 0.9;
//       maxWidth = '900px';
//     } else if (width < 1440) { // Малые и средние десктопы
//       scale = 1;
//       fontScale = 1;
//       paddingScale = 1;
//       maxWidth = '100%';
//     } else if (width < 1920) { // Большие экраны
//       scale = 1.1;
//       fontScale = 1.1;
//       paddingScale = 1.1;
//       maxWidth = '1200px';
//     } else {                  // Очень большие экраны
//       scale = 1.2;
//       fontScale = 1.2;
//       paddingScale = 1.2;
//       maxWidth = '1400px';
//     }
//
//     container.style.transformOrigin = 'top center';
//     container.style.transition = 'transform 0.3s ease';
//
//     // Для мобильных экранов и планшетов применяем transform
//     if (width < 1024) {
//       const translateX = (1 - scale) * window.innerWidth / 2;
//       container.style.transform = `translateX(${translateX}px) scale(${scale})`;
//     } else {
//       // Для больших экранов убираем transform
//       container.style.transform = '';
//     }
//
//     // Меняем максимальную ширину контейнера, если есть конкретный контейнер для контента
//     // Можно заменить 'container' на нужный класс или id в вашем проекте
//     if (container.style.maxWidth !== undefined) {
//       container.style.maxWidth = maxWidth;
//       container.style.margin = '0 auto'; // центрирование при ограничении ширины
//     }
//
//     document.documentElement.style.setProperty('--font-scale', fontScale);
//     document.documentElement.style.setProperty('--padding-scale', paddingScale);
//   }
//
//   document.addEventListener('DOMContentLoaded', adjustScale);
//
//   let resizeTimeout;
//   window.addEventListener('resize', () => {
//     clearTimeout(resizeTimeout);
//     resizeTimeout = setTimeout(adjustScale, 150);
//   });
// })();
