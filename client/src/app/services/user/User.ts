export interface User {
    id: number,
    name: string,
    login: string,
    password?: string,
    birthday: string,
    reg_date: string,
    description: string,
    role: UserRole,
    subs: number,
    to_subs: number,
    materials: number[],
    avatar: string,
    current: boolean,
    sub_by_current: boolean,
    total_rep: number,
    total_likes: number,
    total_views: number,
    total_news: number,
}

export enum UserRole {
    READER = 0,
    AUTHOR = 1,
    MODERATOR = 2,
}