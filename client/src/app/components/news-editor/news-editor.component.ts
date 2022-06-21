import { Component, OnInit } from '@angular/core';
import { FormBuilder } from '@angular/forms';
import { Router } from '@angular/router';
import { AuthService } from '../../services/auth/auth.service';
import { NewsService } from '../../services/news/news.service';

@Component({
  selector: 'app-news-editor',
  templateUrl: './news-editor.component.html',
  styleUrls: ['./news-editor.component.scss']
})
export class NewsEditorComponent implements OnInit {

    newsResource: FormData = new FormData();
    regions?: string[]
    categorys?: string[]
    
    newsForm = this.formBuilder.group({
        title: '',
        content: '',
        region: '',
        category: '',
    });

    constructor(
        private formBuilder: FormBuilder,
        private newsService: NewsService,
        private authService: AuthService,
        private router: Router
    ) { }
    
    ngOnInit(): void {
        this.newsService.getRegions().subscribe(regions => {
            this.regions = regions
        })
        this.newsService.getCategorys().subscribe(categorys => {
            this.categorys = categorys
        })
    }
    
    onSubmit(): void {
        this.newsService.addNews(
            this.newsForm.value.title,
            this.newsForm.value.content,
            this.newsForm.value.region,
            this.newsForm.value.category,
        ).subscribe( (news) => {
            this.newsService.addNewsResource(this.newsResource, news.id).subscribe({
                error: () =>  this.toUserPage(),
                complete: () => this.toUserPage(),
            })
        })
    }
    
    private toUserPage() {
        this.authService.getCurrentId().subscribe(user_id => {
            if (user_id != -1 ) {
                this.router.navigateByUrl("user-page/" + user_id);
            }
        })
    }
    
    onFileSelected(event: any): void {
        const resource = <File>event.target.files[0]
        this.newsResource.append('image', resource, resource.name);
    }
}
