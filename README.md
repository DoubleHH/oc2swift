# oc2swift
Objective-C to Swift code. Objective-C代码转Swift.

注：目前只用于转数据model及enum类型

# 使用方法

1. 打开Terminal，cd到脚本文件夹
2. 输入命令：python oc2swift_model.py oc_header_file_path


# 例子

`python oc2swift_model.py /Users/name/Project/axxx/src/Buyer/Module/Order/Model/BYOrderListModel.h`

### Objective-C

~~~objective-c
typedef NS_ENUM(NSInteger, BYOrderStatus){
    BYOrderStatusAll = -1,            //全部订单，我的订单页面使用
    BYOrderStatusToBePay = 0,         //待付款
    BYOrderStatusCancelPay = 5,       //取消支付
    BYOrderStatusPendingOrder = 10,    //待接单
    BYOrderStatusPendingDelivery = 20, //待发货
    BYOrderStatusToReceiveGoods = 30,  //待收货
    BYOrderStatusCancelled = 90,       //已取消
    BYOrderStatusCompleted  = 100       //已完成
};

typedef NS_ENUM(NSInteger,BYOrderOperationType){
    /// 支付
    BYOrderOperationTypePay = 1,
    /// 取消订单(取消支付)
    BYOrderOperationTypeCancelPay = 2,
    /// 取消订单(取消支付)
    BYOrderOperationTypeCancelOrder = 3,
    /// 查看转账信息
    BYOrderOperationTypeCheckTransferInformation = 4,
    /// 上传凭证
    BYOrderOperationTypeUploadVoucher = 5,
    /// 申请售后
    BYOrderOperationTypeApplyAfterSale = 6,
	/// 售后详情
	BYOrderOperationTypeAfterSaleInfo = 8,
    /// 再次购买
    BYOrderOperationTypeBuyAgain = 9,
    /// 确认收货
    BYOrderOperationTypeConfirmAccept = 10,
    /// 查看凭证
    BYOrderOperationTypeShowVoucher = 11,
};

typedef NS_ENUM(NSUInteger, BYOrderType) {
    BYOrderTypeSales = 1,
    BYOrderTypePurchase = 2,
};

@interface BYOrderBaseModel : JSONModel

- (NSString *_Nullable)parent_order_id;

- (NSString *_Nullable)order_id;

- (NSString *_Nonnull)local_order_id;

- (NSString *_Nonnull)local_order_id_key;

@end

@interface NSString (LocalOrderId)

@property (nonatomic, readonly) BYOrderType by_orderType;
@property (nonatomic, readonly) NSString * _Nonnull logic_order_id;
@property (nonatomic, readonly) NSDictionary * _Nonnull by_orderIdParameters;

@end

@protocol BYMyOrderSkuItemModel @end
@interface BYMyOrderSkuItemModel : JSONModel
/// 单品id
@property(nonatomic, strong, nullable) NSString *sku_id;
/// 单品名字
@property(nonatomic, strong ,nullable) NSString *sku_name;
/// 商品id
@property(nonatomic, strong, nullable) NSString *product_id;
/// 商品名称
@property(nonatomic, strong, nullable) NSString *product_name;
/// 商品图片
@property(nonatomic, strong, nullable) NSString *pic_url;
/// 商品价格(待支付价)
@property(nonatomic, strong, nullable) NSString *final_price;
/// 商品数量
@property (nonatomic, strong, nullable) NSString *sku_number;

@end

@protocol BYOrderOperationModel @end
@interface BYOrderOperationModel : JSONModel

/// 操作id
@property(nonatomic, strong, nullable) NSString *operation_id;
/// 操作名字
@property(nonatomic, strong, nullable) NSString *operation_name;

@end

@protocol BYOrderModel @end
@interface BYOrderModel : BYOrderBaseModel

/// 订单类型 1: 销售单 2: 采购单
@property (nonatomic, assign) BYOrderType order_type;
/// 总价格(待支付价)
@property (nonatomic, strong, nullable) NSString *total_final_price;
/// 总数
@property (nonatomic, strong, nullable) NSString *total_number;
/// 销售单号
@property (nonatomic, strong, nullable) NSString *parent_order_id;
/// 采购单号
@property (nonatomic, strong, nullable) NSString *order_id;
/// 订单状态
@property (nonatomic, strong, nullable) NSString *status;
/// 状态描述
@property (nonatomic, strong, nullable) NSString *status_desc;
/// 支付类型 0: 未选择 1: 在线支付 2: 赊销支付 3: 公对公转账 order_type=1时有此字段
@property (nonatomic, strong, nullable) NSString *pay_type;
/// 下单时间
@property (nonatomic, strong, nullable) NSString *create_time;
/// 是否有售后 0:没有 1:有
@property (nonatomic, strong, nullable) NSString *has_service;
/// sku列表
@property (nonatomic, copy, nullable) NSArray<BYMyOrderSkuItemModel *><BYMyOrderSkuItemModel> *sku_list;
/// 订单操作列表
@property (nonatomic, copy, nullable) NSArray<BYOrderOperationModel *><BYOrderOperationModel> *order_operation;

///自定义
@property (nonatomic, assign) CGFloat cellHeight;

@end

@interface BYOrderListModel : JSONModel

/// 总数
@property (nonatomic, strong, nullable) NSString *total;
/// 订单列表
@property (nonatomic, copy, nullable) NSArray<BYOrderModel *><BYOrderModel> *order_list;

@end
~~~

### Swift

~~~swift
enum BYOrderStatus : Int {
    /// 全部订单，我的订单页面使用
    case all = -1
    /// 待付款
    case toBePay = 0
    /// 取消支付
    case cancelPay = 5
    /// 待接单
    case pendingOrder = 10
    /// 待发货
    case pendingDelivery = 20
    /// 待收货
    case toReceiveGoods = 30
    /// 已取消
    case cancelled = 90
    /// 已完成
    case completed  = 100
}

enum BYOrderOperationType : Int {
    /// 支付
    case pay = 1
    /// 取消订单(取消支付)
    case cancelPay = 2
    /// 取消订单(取消支付)
    case cancelOrder = 3
    /// 查看转账信息
    case checkTransferInformation = 4
    /// 上传凭证
    case uploadVoucher = 5
    /// 申请售后
    case applyAfterSale = 6
    /// 售后详情
    case afterSaleInfo = 8
    /// 再次购买
    case buyAgain = 9
    /// 确认收货
    case confirmAccept = 10
    /// 查看凭证
    case showVoucher = 11
}

enum BYOrderType : Int {
    case sales = 1
    case purchase = 2
}

struct BYOrderBaseModel: Codable {
}

struct NSString (LocalOrderId): Codable {
    var BYOrderType by_orderType: BYOrderType by_orderType?
    var _Nonnull logic_order_id: String?
    var _Nonnull by_orderIdParameters: Dictionary?
}

struct BYMyOrderSkuItemModel: Codable {
    /// 单品id
    var sku_id: String?
    /// 单品名字
    var sku_name: String?
    /// 商品id
    var product_id: String?
    /// 商品名称
    var product_name: String?
    /// 商品图片
    var pic_url: String?
    /// 商品价格(待支付价)
    var final_price: String?
    /// 商品数量
    var sku_number: String?
}

struct BYOrderOperationModel: Codable {
    /// 操作id
    var operation_id: String?
    /// 操作名字
    var operation_name: String?
}

struct BYOrderModel: Codable {
    /// 订单类型 1: 销售单 2: 采购单
    var BYOrderType order_type: BYOrderType order_type?
    /// 总价格(待支付价)
    var total_final_price: String?
    /// 总数
    var total_number: String?
    /// 销售单号
    var parent_order_id: String?
    /// 采购单号
    var order_id: String?
    /// 订单状态
    var status: String?
    /// 状态描述
    var status_desc: String?
    /// 支付类型 0: 未选择 1: 在线支付 2: 赊销支付 3: 公对公转账 order_type=1时有此字段
    var pay_type: String?
    /// 下单时间
    var create_time: String?
    /// 是否有售后 0:没有 1:有
    var has_service: String?
    /// sku列表
    var sku_list: Array<BYMyOrderSkuItemModel>?
    /// 订单操作列表
    var order_operation: Array<BYOrderOperationModel>?
    ///自定义
    var CGFloat cellHeight: CGFloat cellHeight?
}

struct BYOrderListModel: Codable {
    /// 总数
    var total: String?
    /// 订单列表
    var order_list: Array<BYOrderModel>?
}
~~~
