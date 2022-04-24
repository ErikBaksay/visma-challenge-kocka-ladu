import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-upload',
  templateUrl: './upload.component.html',
  styleUrls: ['./upload.component.sass']
})
export class UploadComponent implements OnInit {

  categories = ['Newcomers', 'New Projects', 'Tournaments', 'Sport Challenges', 'Other events']
  routes = ['newcomers', 'new-projects', 'tournaments', 'sport-challenges', 'other-events']

  constructor() { }

  ngOnInit(): void {
    document.querySelector<HTMLInputElement>("#date")!.valueAsDate = new Date();
  }

}
