import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { HttpClientModule } from '@angular/common/http';
import { AppRoutingModule } from './app-routing.module';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';

import { MatIconModule } from '@angular/material/icon';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import {MatSelectModule} from '@angular/material/select';
import {MatSlideToggleModule} from '@angular/material/slide-toggle'; 

import { AngularEditorModule } from '@kolkov/angular-editor';

import { AppComponent } from './components/app/app.component';
import { CommentComponent } from './components/comment/comment.component';
import { NewsShortInfoComponent } from './components/news-short-info/news-short-info.component';
import { NewsListComponent } from './components/news-list/news-list.component';
import { NewsPageComponent } from './components/news-page/news-page.component';
import { UserListComponent } from './components/user-list/user-list.component';
import { UserPageComponent } from './components/user-page/user-page.component';
import { UserShortInfoComponent } from './components/user-short-info/user-short-info.component';
import { LoginFormComponent } from './components/login-form/login-form.component';
import { RegFormComponent } from './components/reg-form/reg-form.component';
import { NewsEditorComponent } from './components/news-editor/news-editor.component';
import { UserMenuComponent } from './components/user-menu/user-menu.component';
import { NewsFilterComponent } from './components/news-filter/news-filter.component';
import { UserFilterComponent } from './components/user-filter/user-filter.component';

@NgModule({
  declarations: [
    AppComponent,
    NewsShortInfoComponent,
    NewsListComponent,
    NewsPageComponent,
    UserListComponent,
    UserPageComponent,
    UserShortInfoComponent,
    LoginFormComponent,
    RegFormComponent,
    NewsEditorComponent,
    CommentComponent,
    UserMenuComponent,
    NewsFilterComponent,
    UserFilterComponent,
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    FormsModule,
    ReactiveFormsModule,
    HttpClientModule,
    MatIconModule,
    MatInputModule,
    MatButtonModule,
    BrowserAnimationsModule,
    AngularEditorModule,
    MatSelectModule,
    MatSlideToggleModule,
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
