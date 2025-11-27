"""
展示所有模板清单
"""
from app.utils.db import get_db_session
from app.models.template import Template

def main():
    db = get_db_session()
    
    # 查询所有模板
    templates = db.query(Template).order_by(
        Template.category, 
        Template.sort_order.desc()
    ).all()
    
    print('\n🎉 模板库完整清单 (50个模板)\n')
    print('='*100)
    
    # 分类名称映射
    cat_names = {
        'sequence': '🔄 顺序型',
        'list': '📋 列表型',
        'comparison': '⚖️ 对比型',
        'relation': '🔗 关系型',
        'hierarchy': '🏔️ 层级型',
        'chart': '📊 图表型',
        'quadrant': '🎯 四象限型'
    }
    
    current_cat = ''
    i = 0
    
    for t in templates:
        # 新分类时打印分类标题
        if t.category != current_cat:
            current_cat = t.category
            print(f'\n{cat_names.get(current_cat, current_cat)}')
            i = 0
        
        i += 1
        print(f'  {i:2d}. {t.name} ({t.id})')
    
    print('\n' + '='*100)
    print(f'\n✅ 总计: {len(templates)}个模板')
    
    # 统计
    from sqlalchemy import func
    stats = db.query(
        Template.category, 
        func.count(Template.id)
    ).group_by(
        Template.category
    ).order_by(
        func.count(Template.id).desc()
    ).all()
    
    print('\n📊 分类统计:')
    for cat, count in stats:
        print(f'  {cat_names.get(cat, cat)}: {count}个')
    
    db.close()

if __name__ == '__main__':
    main()
