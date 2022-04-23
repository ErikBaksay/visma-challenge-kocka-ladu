import { Component, OnInit } from '@angular/core';
import { images_data } from 'src/database';

@Component({
  selector: 'app-gallery',
  templateUrl: './gallery.component.html',
  styleUrls: ['./gallery.component.sass']
})
export class GalleryComponent implements OnInit {

  images_data = images_data
  parallax_types = ['parallaxSlow', 'parallaxMedium', 'parallaxHigh']

  constructor() { }

  ngOnInit(): void {
    function getRandomInt(max: number) {
      return Math.floor(Math.random() * max);
    }

    console.log(getRandomInt(30) + 50);

    const imageCards = document.getElementsByClassName("imageCard")

    for (var i = 0; i < imageCards.length; i++) {
      console.log(imageCards[i]);
    }
  }
}
