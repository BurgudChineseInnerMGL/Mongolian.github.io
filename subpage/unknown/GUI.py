import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import os

class DataManager:
    def __init__(self, root):
        self.root = root
        self.root.title("JSON 数据管理系统")
        self.root.geometry("800x600")
        
        # 数据存储
        self.data = []
        self.filtered_data = []
        self.current_file = "data.json"
        
        # 创建界面
        self.create_widgets()
        
        # 加载数据
        self.load_data()
    
    def create_widgets(self):
        # 主框架
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 配置网格权重
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(5, weight=1)
        
        # 文件操作区域
        file_frame = ttk.LabelFrame(main_frame, text="文件操作", padding="5")
        file_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        file_frame.columnconfigure(1, weight=1)
        
        ttk.Button(file_frame, text="导入 JSON", command=self.import_json).grid(row=0, column=0, padx=(0, 5))
        ttk.Button(file_frame, text="保存数据", command=self.save_data).grid(row=0, column=1, padx=5)
        ttk.Button(file_frame, text="导出 JSON", command=self.export_json).grid(row=0, column=2, padx=5)
        
        # 数据输入区域
        input_frame = ttk.LabelFrame(main_frame, text="数据输入", padding="5")
        input_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        input_frame.columnconfigure(1, weight=1)
        
        ttk.Label(input_frame, text="1:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.topic_entry = ttk.Entry(input_frame)
        self.topic_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=2, padx=(5, 0))
        
        ttk.Label(input_frame, text="2:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.category_entry = ttk.Entry(input_frame)
        self.category_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=2, padx=(5, 0))
        
        ttk.Label(input_frame, text="3:").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.description_entry = ttk.Entry(input_frame)
        self.description_entry.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=2, padx=(5, 0))
        
        ttk.Label(input_frame, text="4:").grid(row=3, column=0, sticky=tk.W, pady=2)
        self.importance_entry = ttk.Entry(input_frame)
        self.importance_entry.grid(row=3, column=1, sticky=(tk.W, tk.E), pady=2, padx=(5, 0))
        
        # 按钮区域
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Button(button_frame, text="添加数据", command=self.add_item).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text="删除选中", command=self.delete_item).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="清空输入", command=self.clear_entries).pack(side=tk.LEFT, padx=5)
        
        # 搜索区域
        search_frame = ttk.Frame(main_frame)
        search_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(search_frame, text="搜索:").pack(side=tk.LEFT)
        self.search_entry = ttk.Entry(search_frame)
        self.search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 5))
        self.search_entry.bind('<KeyRelease>', self.search_items)
        
        ttk.Button(search_frame, text="清除搜索", command=self.clear_search).pack(side=tk.LEFT)
        
        # 数据显示区域
        data_frame = ttk.LabelFrame(main_frame, text="数据列表", padding="5")
        data_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        data_frame.columnconfigure(0, weight=1)
        data_frame.rowconfigure(0, weight=1)
        
        # 创建树形视图
        columns = ("ID", "1", "2", "3", "4")
        self.tree = ttk.Treeview(data_frame, columns=columns, show="headings", height=15)
        
        # 设置列标题
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100, anchor=tk.CENTER)
        
        # 添加滚动条
        scrollbar = ttk.Scrollbar(data_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # 布局树形视图和滚动条
        self.tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # 状态栏
        self.status_var = tk.StringVar()
        self.status_var.set("就绪")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN)
        status_bar.grid(row=5, column=0, columnspan=2, sticky=(tk.W, tk.E))
    
    def load_data(self, filename=None):
        """加载数据从JSON文件"""
        if filename:
            self.current_file = filename
        
        try:
            if os.path.exists(self.current_file):
                with open(self.current_file, 'r', encoding='utf-8') as file:
                    self.data = json.load(file)
                self.status_var.set(f"已加载 {len(self.data)} 条数据从 {self.current_file}")
            else:
                self.data = []
                self.status_var.set("数据文件不存在，已创建空数据集")
        except Exception as e:
            messagebox.showerror("错误", f"加载数据时出错: {str(e)}")
            self.data = []
        
        self.filtered_data = self.data.copy()
        self.update_treeview()
    
    def save_data(self):
        """保存数据到JSON文件"""
        try:
            with open(self.current_file, 'w', encoding='utf-8') as file:
                json.dump(self.data, file, ensure_ascii=False, indent=2)
            self.status_var.set(f"数据已保存到 {self.current_file}")
        except Exception as e:
            messagebox.showerror("错误", f"保存数据时出错: {str(e)}")
    
    def import_json(self):
        """导入JSON文件"""
        filename = filedialog.askopenfilename(
            title="选择JSON文件",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if filename:
            self.load_data(filename)
    
    def export_json(self):
        """导出数据到JSON文件"""
        filename = filedialog.asksaveasfilename(
            title="保存JSON文件",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as file:
                    json.dump(self.data, file, ensure_ascii=False, indent=2)
                self.status_var.set(f"数据已导出到 {filename}")
            except Exception as e:
                messagebox.showerror("错误", f"导出数据时出错: {str(e)}")
    
    def add_item(self):
        """添加新数据项"""
        topic = self.topic_entry.get().strip()
        category = self.category_entry.get().strip()
        description = self.description_entry.get().strip()
        importance = self.importance_entry.get().strip()
        
        if not topic or not category or not description or not importance:
            messagebox.showwarning("输入错误", "请填写所有字段")
            return
        
        # 生成新ID
        new_id = max([item.get('id', 0) for item in self.data]) + 1 if self.data else 1
        
        # 创建新项目
        new_item = {
            "id": new_id,
            "topic": topic,
            "category": category,
            "description": description,
            "importance": importance
        }
        
        # 添加到数据列表
        self.data.append(new_item)
        self.filtered_data = self.data.copy()
        
        # 更新显示
        self.update_treeview()
        self.clear_entries()
        self.status_var.set(f"已添加新数据项 (ID: {new_id})")
    
    def delete_item(self):
        """删除选中的数据项"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("选择错误", "请先选择要删除的数据项")
            return
        
        # 确认删除
        if not messagebox.askyesno("确认删除", "确定要删除选中的数据项吗？"):
            return
        
        # 获取选中的ID
        selected_ids = []
        for item in selected:
            item_id = int(self.tree.item(item)['values'][0])
            selected_ids.append(item_id)
        
        # 从数据中删除
        self.data = [item for item in self.data if item['id'] not in selected_ids]
        self.filtered_data = self.data.copy()
        
        # 更新显示
        self.update_treeview()
        self.status_var.set(f"已删除 {len(selected_ids)} 条数据")
    
    def search_items(self, event=None):
        """搜索数据项"""
        search_term = self.search_entry.get().strip().lower()
        
        if not search_term:
            self.filtered_data = self.data.copy()
        else:
            self.filtered_data = [
                item for item in self.data
                if (search_term in str(item.get('topic', '')).lower() or
                    search_term in str(item.get('category', '')).lower() or
                    search_term in str(item.get('description', '')).lower() or
                    search_term in str(item.get('importance', '')).lower())
            ]
        
        self.update_treeview()
        self.status_var.set(f"找到 {len(self.filtered_data)} 条匹配的数据")
    
    def clear_search(self):
        """清除搜索"""
        self.search_entry.delete(0, tk.END)
        self.filtered_data = self.data.copy()
        self.update_treeview()
        self.status_var.set("搜索已清除")
    
    def clear_entries(self):
        """清空输入字段"""
        self.topic_entry.delete(0, tk.END)
        self.category_entry.delete(0, tk.END)
        self.description_entry.delete(0, tk.END)
        self.importance_entry.delete(0, tk.END)
    
    def update_treeview(self):
        """更新树形视图显示"""
        # 清空现有数据
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # 添加新数据
        for item in self.filtered_data:
            self.tree.insert('', tk.END, values=(
                item.get('id', ''),
                item.get('topic', ''),
                item.get('category', ''),
                item.get('description', ''),
                item.get('importance', '')
            ))

def main():
    root = tk.Tk()
    app = DataManager(root)
    root.mainloop()

if __name__ == "__main__":
    main()