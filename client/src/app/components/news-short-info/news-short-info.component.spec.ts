import { ComponentFixture, TestBed } from '@angular/core/testing';

import { NewsShortInfoComponent } from './news-short-info.component';

describe('NewsShortInfoComponent', () => {
  let component: NewsShortInfoComponent;
  let fixture: ComponentFixture<NewsShortInfoComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ NewsShortInfoComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(NewsShortInfoComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
