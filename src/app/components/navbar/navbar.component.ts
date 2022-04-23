import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-navbar',
  templateUrl: './navbar.component.html',
  styleUrls: ['./navbar.component.sass']
})
export class NavbarComponent implements OnInit {

  constructor() { }

  ngOnInit(): void {
  }
  menuOpen(){
    let menu = document.getElementById("collapsableMenu")
    if (menu!.style.display == "none"){
      menu!.style.display = "block"
    }else{
      menu!.style.display = "none"
    }
  }
}
