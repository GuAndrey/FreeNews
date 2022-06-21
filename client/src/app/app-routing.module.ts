import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { NewsEditorComponent } from './components/news-editor/news-editor.component';
import { NewsListComponent } from './components/news-list/news-list.component';
import { NewsPageComponent } from './components/news-page/news-page.component';
import { UserListComponent } from './components/user-list/user-list.component';
import { UserPageComponent } from './components/user-page/user-page.component';

const routes: Routes = [
  { path: '', redirectTo: '/news-list', pathMatch: 'full' },
  { path: 'news-page/editor', component: NewsEditorComponent },
  { path: 'news-page/:id', component: NewsPageComponent },
  { path: 'news-list', component: NewsListComponent },
  { path: 'user-page/:id', component: UserPageComponent },
  { path: 'user-list', component: UserListComponent }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
